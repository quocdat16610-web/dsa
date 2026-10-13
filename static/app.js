// Ứng dụng một trang: lộ trình, giáo án, lý thuyết, mô phỏng, video, bài tập, chấm bài, tổng hợp đề.
(function () {
  "use strict";
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const app = $("#app");
  const store = {
    get(k, d) { try { const v = localStorage.getItem("dsa." + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem("dsa." + k, JSON.stringify(v)); } catch (e) { /* bỏ qua */ } },
  };
  const LV_NAME = { 1: "Cơ bản", 2: "Dễ", 3: "Trung bình", 4: "Khá", 5: "Nâng cao" };
  const CAT_VAR = { "Cơ bản": "--c-basic", "Thuật toán": "--c-algo", "CTDL": "--c-ds", "Đồ thị": "--c-graph" };
  let META = null, PROB = {}, TOPIC = {};
  let user = store.get("user", "khách");
  let solved = new Set(store.get("solved." + user, []));
  let tried = new Set(store.get("tried." + user, []));

  // ------------------------------------------------------------ tiện ích
  async function api(path, body) {
    const opt = body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {};
    const r = await fetch(path, opt);
    const j = await r.json().catch(() => ({ error: "Phản hồi không hợp lệ" }));
    if (!r.ok) throw new Error(j.error || r.statusText);
    return j;
  }
  const lvBadge = l => `<span class="lv lv${l}">${LV_NAME[l]}</span>`;
  const catColor = c => `var(${CAT_VAR[c] || "--accent"})`;
  function markSolved(pid, ok) {
    tried.add(pid); store.set("tried." + user, [...tried]);
    if (ok) { solved.add(pid); store.set("solved." + user, [...solved]); }
  }
  function status(pid) {
    if (solved.has(pid)) return '<span class="solved-mark" title="Đã giải">✓</span>';
    if (tried.has(pid)) return '<span style="color:var(--bad)" title="Đã thử">✗</span>';
    return "";
  }
  function setNav(name) { $$(".nav a").forEach(a => a.classList.toggle("active", a.dataset.nav === name)); }
  function copyText(t, btn) {
    navigator.clipboard?.writeText(t).then(() => { if (btn) { const o = btn.textContent; btn.textContent = "Đã chép"; setTimeout(() => btn.textContent = o, 1200); } });
  }
  document.addEventListener("click", e => {
    const b = e.target.closest("pre.code .copy");
    if (b) copyText(b.parentElement.querySelector("code").innerText, b);
  });
  function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
  function shuffle(a, r) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  // ------------------------------------------------------------ chủ đề sáng/tối, người dùng
  const theme = store.get("theme", null);
  if (theme) document.documentElement.dataset.theme = theme;
  $("#themeBtn").onclick = () => {
    const dark = document.documentElement.dataset.theme === "dark" ||
      (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.dataset.theme = dark ? "light" : "dark";
    store.set("theme", document.documentElement.dataset.theme);
  };
  $("#userName").textContent = user;
  $("#userBtn").onclick = () => {
    const n = prompt("Nhập tên của bạn (dùng để lưu bài nộp và tiến độ):", user);
    if (n && n.trim()) {
      user = n.trim().slice(0, 40); store.set("user", user); $("#userName").textContent = user;
      solved = new Set(store.get("solved." + user, [])); tried = new Set(store.get("tried." + user, []));
      syncSolved().then(route);
    }
  };
  async function syncSolved() {
    try {
      const subs = await api("/api/submissions?limit=100000&user=" + encodeURIComponent(user));
      subs.forEach(s => { tried.add(s.pid); if (s.ok) solved.add(s.pid); });
      store.set("solved." + user, [...solved]); store.set("tried." + user, [...tried]);
    } catch (e) { /* máy chủ chưa có bài nộp */ }
  }

  // ------------------------------------------------------------ định tuyến
  async function route() {
    const h = location.hash.replace(/^#\/?/, "");
    const [page, a, b] = h.split("/");
    window.scrollTo(0, 0);
    try {
      if (!page) return home();
      if (page === "topic") return topicPage(+a, b || "giao-an");
      if (page === "problem") return problemPage(a);
      if (page === "problems") return problemsPage();
      if (page === "plan") return planPage();
      if (page === "contest") return contestPage(a);
      if (page === "submissions") return subsPage();
      home();
    } catch (e) { app.innerHTML = `<div class="panel">Lỗi: ${esc(e.message)}</div>`; }
  }
  window.addEventListener("hashchange", route);

  // ------------------------------------------------------------ trang chủ (lộ trình)
  function home() {
    setNav("home");
    const total = META.problems.length;
    let html = `<section class="hero"><div><div class="kicker">Kiến thức dự kiến</div>
      <h1>Lộ trình dự kiến của lớp học</h1>
      <div class="muted">20 chuyên đề từ cơ bản đến nâng cao · ${total} bài tập chấm tự động kiểu Codeforces · có giáo án, lý thuyết, mô phỏng và video.</div></div>
      <div class="stats"><div class="stat"><b>20</b><span class="muted small">chuyên đề</span></div>
      <div class="stat"><b>${total}</b><span class="muted small">bài tập</span></div>
      <div class="stat"><b>${solved.size}</b><span class="muted small">bạn đã giải</span></div></div></section>
      <div class="legend">${Object.keys(CAT_VAR).map(c => `<span style="--c:${catColor(c)}">${c}</span>`).join("")}</div>
      <div class="road">`;
    META.topics.forEach((t, i) => {
      const row = Math.floor(i / 4), colIdx = i % 4, col = row % 2 === 0 ? colIdx + 1 : 4 - colIdx;
      const probs = META.problems.filter(p => p.topic === t.id);
      const done = probs.filter(p => solved.has(p.id)).length;
      const cls = ["node"];
      if (row % 2 === 1) cls.push("rev");
      if (colIdx === 3) cls.push("last-in-row", "turn");
      if (i === META.topics.length - 1) cls.push("end");
      html += `<a class="${cls.join(" ")}" href="#/topic/${t.id}" style="--cc:${catColor(t.cat)};grid-row:${row + 1};grid-column:${col}">
        <div class="row"><span class="num">${t.id}</span><span class="cat">${esc(t.cat)}</span></div>
        <div class="nm">${esc(t.short)}</div>
        <div class="meta"><span>${probs.length} bài</span><span>${done}/${probs.length} đã giải</span></div>
        <div class="bar"><i style="width:${probs.length ? 100 * done / probs.length : 0}%"></i></div></a>`;
    });
    html += `</div><p class="muted small" style="margin-top:18px">Mẹo: bấm vào một chuyên đề để xem giáo án theo buổi, lý thuyết, mô phỏng thuật toán, video và danh sách bài tập.
      Dùng <a href="#/contest">Tổng hợp đề</a> để tạo đề kiểm tra trộn nhiều chuyên đề liên quan.</p>`;
    app.innerHTML = html;
  }

  // ------------------------------------------------------------ giáo án toàn khoá
  function planPage() {
    setNav("plan");
    let html = `<div class="row"><h1 class="grow">Giáo án toàn khoá</h1>
      <button class="btn no-print" onclick="window.print()">🖨 In / Lưu PDF</button></div>
      <p class="muted">Mỗi chuyên đề gồm 2 buổi × 120 phút. Bấm tên chuyên đề để xem giáo án chi tiết và bài tập về nhà.</p>
      <div class="panel"><table class="list"><thead><tr><th>#</th><th>Chuyên đề</th><th>Mảng</th><th>Mục tiêu chính</th><th>Buổi 1</th><th>Buổi 2</th><th>Bài</th></tr></thead><tbody>`;
    META.topics.forEach(t => {
      html += `<tr><td><b>${t.id}</b></td><td><a href="#/topic/${t.id}/giao-an">${esc(t.name)}</a></td>
        <td><span class="badge" style="color:${catColor(t.cat)};border-color:${catColor(t.cat)}">${esc(t.cat)}</span></td>
        <td class="small">${t.goals.slice(0, 2).map(esc).join("<br>")}</td>
        <td class="small">${t.b1.map(esc).join("; ")}</td><td class="small">${t.b2.map(esc).join("; ")}</td><td>${t.count}</td></tr>`;
    });
    html += `</tbody></table></div>`;
    app.innerHTML = html;
  }

  // ------------------------------------------------------------ trang chuyên đề
  async function topicPage(id, tab) {
    setNav("home");
    if (!TOPIC[id]) TOPIC[id] = await api("/api/topic/" + id);
    const t = TOPIC[id];
    const tabs = [["giao-an", "Giáo án"], ["ly-thuyet", "Lý thuyết"], ["mo-phong", "Mô phỏng"], ["video", "Video"],
      ["bai-tap", `Bài tập (${t.problems.length})`], ["luyen-them", "Luyện thêm"]];
    const prev = META.topics.find(x => x.id === id - 1), next = META.topics.find(x => x.id === id + 1);
    app.innerHTML = `<div class="topic-head" style="--cc:${catColor(t.cat)}"><div class="num">${t.id}</div>
      <div class="grow"><div class="muted small">${esc(t.cat)}</div><h1 style="margin:0">${esc(t.name)}</h1></div>
      <div class="row no-print">${prev ? `<a class="btn" href="#/topic/${prev.id}/${tab}">← ${prev.id}</a>` : ""}${next ? `<a class="btn" href="#/topic/${next.id}/${tab}">${next.id} →</a>` : ""}</div></div>
      <div class="tabs">${tabs.map(([k, v]) => `<button data-tab="${k}" class="${k === tab ? "active" : ""}">${v}</button>`).join("")}</div>
      <div id="tabBody"></div>`;
    $$(".tabs button").forEach(b => b.onclick = () => { location.hash = `#/topic/${id}/${b.dataset.tab}`; });
    const body = $("#tabBody");
    if (tab === "giao-an") body.innerHTML = lessonPlan(t);
    else if (tab === "ly-thuyet") body.innerHTML = `<div class="panel theory">${MD.render(t.theory)}</div>`;
    else if (tab === "mo-phong") { body.innerHTML = `<div class="panel"><div id="vizMount"></div></div>`; VIZ.mount($("#vizMount"), t.viz); }
    else if (tab === "video") videoTab(body, t);
    else if (tab === "bai-tap") body.innerHTML = problemTable(t.problems, true);
    else if (tab === "luyen-them") practiceTab(body, t);
  }

  function homework(t) {
    const by = l => t.problems.filter(p => p.level === l);
    const pick = (ls, n) => ls.flatMap(by).slice(0, n);
    return [["Buổi 1 — luyện tại lớp", pick([1], 4)], ["Buổi 1 — bài tập về nhà", pick([2], 5)],
      ["Buổi 2 — luyện tại lớp", pick([3], 5)], ["Buổi 2 — bài tập về nhà", pick([4], 4)], ["Thử thách (học sinh giỏi)", pick([5], 3)]];
  }
  function lessonPlan(t) {
    let h = `<div class="panel"><div class="row"><h2 class="grow" style="margin:0">Giáo án: ${esc(t.name)}</h2>
      <button class="btn no-print" onclick="window.print()">🖨 In giáo án</button></div>
      <h3>Mục tiêu</h3><ul class="goals">${t.goals.map(g => `<li>${esc(g)}</li>`).join("")}</ul>
      <h3>Tiến trình dạy học</h3>`;
    t.sessions.forEach(s => {
      h += `<div class="session"><h3><span>${esc(s.title)}</span><span class="muted small">${s.minutes} phút</span></h3><table>`;
      s.items.forEach(it => { h += `<tr><td>${it.min} phút</td><td>${esc(it.what)}</td></tr>`; });
      h += `</table></div>`;
    });
    h += `<h3>Bài tập theo buổi</h3><div class="hw-list">`;
    homework(t).forEach(([title, ps]) => {
      if (!ps.length) return;
      h += `<div style="break-inside:avoid"><b>${title}</b><ul>${ps.map(p => `<li>${status(p.id)} <a href="#/problem/${p.id}">${p.id} — ${esc(p.title)}</a> ${lvBadge(p.level)}</li>`).join("")}</ul></div>`;
    });
    h += `</div><h3>Đánh giá</h3><ul><li>Hoàn thành ≥ 70% bài mức Cơ bản – Trung bình của chuyên đề.</li>
      <li>Bài kiểm tra 15 phút cuối buổi 2 (tạo ở mục <a href="#/contest/new?topics=${t.id}">Tổng hợp đề</a>).</li>
      <li>Tự giải thích được độ phức tạp thuật toán của bài mình nộp.</li></ul></div>`;
    return h;
  }

  function ytEmbed(url) {
    const m = url.match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{11})/);
    const list = url.match(/[?&]list=([\w-]+)/);
    if (m) return "https://www.youtube-nocookie.com/embed/" + m[1];
    if (list) return "https://www.youtube-nocookie.com/embed/videoseries?list=" + list[1];
    return null;
  }
  function videoTab(body, t) {
    const key = "videos." + t.id;
    const draw = () => {
      const mine = store.get(key, []);
      const vi = t.videos.filter(v => v.lang === "vi"), en = t.videos.filter(v => v.lang !== "vi");
      const card = v => `<a class="video-card" href="${esc(v.url)}" target="_blank" rel="noopener"><span class="yt">▶</span>
        <span><b>${esc(v.author)}</b><br><span class="small muted">${esc(v.title.replace(v.author + ": ", ""))}</span></span></a>`;
      body.innerHTML = `<div class="panel"><h3 style="margin-top:0">🇻🇳 Video tiếng Việt</h3><div class="video-grid">${vi.map(card).join("")}</div>
        <h3>🇮🇳 Giảng viên Ấn Độ (tiếng Anh / Hindi — có thể bật phụ đề tự dịch tiếng Việt)</h3><div class="video-grid">${en.map(card).join("")}</div>
        <p class="small muted">Các liên kết mở trang tìm kiếm YouTube theo đúng chủ đề để luôn có video mới nhất. Giáo viên có thể dán link video cụ thể bên dưới để nhúng trực tiếp cho lớp.</p>
        <h3>Video do giáo viên chọn</h3>
        <form id="vidForm" class="row no-print"><input id="vidUrl" class="grow" placeholder="Dán link YouTube (video hoặc playlist)…">
        <input id="vidTitle" placeholder="Tiêu đề (tuỳ chọn)"><button class="btn primary">Thêm</button></form>
        <div id="vidList" style="display:grid;gap:16px;margin-top:14px"></div></div>`;
      $("#vidList").innerHTML = mine.length ? mine.map((v, i) => {
        const em = ytEmbed(v.url);
        return `<div><div class="row"><b class="grow">${esc(v.title || v.url)}</b><a href="${esc(v.url)}" target="_blank" rel="noopener" class="small">Mở trên YouTube</a>
          <button class="btn no-print" data-del="${i}">Xoá</button></div>
          ${em ? `<div class="embed" style="max-width:720px;margin-top:6px"><iframe src="${em}" allowfullscreen loading="lazy" title="${esc(v.title || "video")}"></iframe></div>` : ""}</div>`;
      }).join("") : `<div class="muted small">Chưa có video nào.</div>`;
      $("#vidForm").onsubmit = e => {
        e.preventDefault();
        const url = $("#vidUrl").value.trim(); if (!/^https?:\/\//.test(url)) return alert("Link không hợp lệ");
        store.set(key, [...mine, { url, title: $("#vidTitle").value.trim() }]); draw();
      };
      $$("[data-del]").forEach(b => b.onclick = () => { mine.splice(+b.dataset.del, 1); store.set(key, mine); draw(); });
    };
    draw();
  }

  function practiceTab(body, t) {
    const related = META.topics.filter(x => x.id !== t.id && (x.cat === t.cat || Math.abs(x.id - t.id) === 1));
    body.innerHTML = `<div class="panel"><h3 style="margin-top:0">Bài luyện thêm trên các trang chấm trực tuyến</h3>
      <ul>${t.practice.map(p => `<li><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.name)}</a></li>`).join("")}
      <li><a href="https://oj.vnoi.info/problems/" target="_blank" rel="noopener">VNOJ — kho bài tiếng Việt</a></li>
      <li><a href="https://codeforces.com/edu/courses" target="_blank" rel="noopener">Codeforces EDU</a></li></ul>
      <h3>Đề tổng hợp kiến thức liên quan</h3>
      <p class="muted">Trộn bài của chuyên đề này với các chuyên đề liên quan: ${related.map(x => esc(x.name)).join(", ")}.</p>
      <a class="btn primary" href="#/contest/new?topics=${[t.id, ...related.map(x => x.id)].join(",")}">Tạo đề tổng hợp</a></div>`;
  }

  // ------------------------------------------------------------ danh sách bài
  function problemTable(list, showTopic) {
    if (!list.length) return `<div class="empty">Không có bài nào.</div>`;
    return `<div class="panel" style="padding:6px 8px"><table class="list"><thead><tr><th></th><th>Mã</th><th>Tên bài</th>${showTopic ? "" : "<th>Chuyên đề</th>"}<th>Mức độ</th><th>Thẻ</th></tr></thead><tbody>
      ${list.map(p => `<tr><td>${status(p.id)}</td><td class="mono">${p.id}</td><td><a href="#/problem/${p.id}">${esc(p.title)}</a></td>
      ${showTopic ? "" : `<td class="small"><a href="#/topic/${p.topic}/bai-tap">${p.topic}. ${esc(META.topics[p.topic - 1].name)}</a></td>`}
      <td>${lvBadge(p.level)}</td><td>${p.tags.map(g => `<span class="tag" data-tag="${esc(g)}">${esc(g)}</span>`).join("")}</td></tr>`).join("")}
      </tbody></table></div>`;
  }
  function problemsPage() {
    setNav("problems");
    const st = store.get("filters", { topic: "", levels: [], q: "", status: "" });
    app.innerHTML = `<h1>Ngân hàng bài tập</h1><div class="filters">
      <input type="search" id="fq" placeholder="Tìm theo tên, mã, thẻ…" value="${esc(st.q)}">
      <select id="ft"><option value="">Tất cả chuyên đề</option>${META.topics.map(t => `<option value="${t.id}" ${+st.topic === t.id ? "selected" : ""}>${t.id}. ${esc(t.name)}</option>`).join("")}</select>
      <span class="level-pills">${[1, 2, 3, 4, 5].map(l => `<button data-l="${l}" class="${st.levels.includes(l) ? "on" : ""}">${LV_NAME[l]}</button>`).join(" ")}</span>
      <select id="fs"><option value="">Mọi trạng thái</option><option value="todo" ${st.status === "todo" ? "selected" : ""}>Chưa giải</option><option value="done" ${st.status === "done" ? "selected" : ""}>Đã giải</option></select>
      <span id="fcount" class="muted small"></span></div><div id="plist"></div>`;
    const draw = () => {
      const q = st.q.toLowerCase();
      const list = META.problems.filter(p => (!st.topic || p.topic === +st.topic) && (!st.levels.length || st.levels.includes(p.level)) &&
        (!q || (p.id + " " + p.title + " " + p.tags.join(" ")).toLowerCase().includes(q)) &&
        (!st.status || (st.status === "done") === solved.has(p.id)));
      $("#plist").innerHTML = problemTable(list, false);
      $("#fcount").textContent = list.length + " bài";
      $$("#plist .tag").forEach(t => t.onclick = () => { st.q = t.dataset.tag; $("#fq").value = st.q; save(); });
    };
    const save = () => { store.set("filters", st); draw(); };
    $("#fq").oninput = e => { st.q = e.target.value; save(); };
    $("#ft").onchange = e => { st.topic = e.target.value; save(); };
    $("#fs").onchange = e => { st.status = e.target.value; save(); };
    $$(".level-pills button").forEach(b => b.onclick = () => {
      const l = +b.dataset.l; st.levels = st.levels.includes(l) ? st.levels.filter(x => x !== l) : [...st.levels, l];
      b.classList.toggle("on"); save();
    });
    draw();
  }

  // ------------------------------------------------------------ trang bài + trình soạn code
  const TEMPLATES = {
    cpp: "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    \n    return 0;\n}\n",
    py: "import sys\ninput = sys.stdin.readline\n\n\ndef main():\n    data = sys.stdin.read().split()\n    \n\n\nmain()\n",
  };
  function setupEditor(ta, gutter, onSubmit) {
    const sync = () => {
      const n = ta.value.split("\n").length;
      gutter.textContent = Array.from({ length: n }, (_, i) => i + 1).join("\n");
      gutter.scrollTop = ta.scrollTop;
    };
    ta.addEventListener("input", sync);
    ta.addEventListener("scroll", () => { gutter.scrollTop = ta.scrollTop; });
    ta.addEventListener("keydown", e => {
      const s = ta.selectionStart, en = ta.selectionEnd, v = ta.value;
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); onSubmit(); return; }
      if (e.key === "Tab") {
        e.preventDefault();
        if (s !== en && v.slice(s, en).includes("\n")) {
          const ls = v.lastIndexOf("\n", s - 1) + 1, block = v.slice(ls, en);
          const nb = e.shiftKey ? block.replace(/^ {1,4}/gm, "") : block.replace(/^/gm, "    ");
          ta.value = v.slice(0, ls) + nb + v.slice(en); ta.selectionStart = ls; ta.selectionEnd = ls + nb.length;
        } else { ta.setRangeText("    ", s, en, "end"); }
        sync(); return;
      }
      if (e.key === "Enter") {
        const ls = v.lastIndexOf("\n", s - 1) + 1, line = v.slice(ls, s);
        let ind = line.match(/^\s*/)[0];
        if (/[{:(\[]\s*$/.test(line)) ind += "    ";
        e.preventDefault();
        if (v[s] === "}" && /\{\s*$/.test(line)) {
          ta.setRangeText("\n" + ind + "\n" + ind.slice(4), s, en, "start");
          ta.selectionStart = ta.selectionEnd = s + 1 + ind.length;
        } else ta.setRangeText("\n" + ind, s, en, "end");
        sync(); return;
      }
      if (e.key === "}") {
        const ls = v.lastIndexOf("\n", s - 1) + 1, line = v.slice(ls, s);
        if (/^\s+$/.test(line) && line.length >= 4) { e.preventDefault(); ta.setRangeText(line.slice(4) + "}", ls, en, "end"); sync(); }
      }
    });
    sync();
    return sync;
  }

  async function problemPage(pid) {
    setNav("problems");
    const p = PROB[pid] || (PROB[pid] = await api("/api/problem/" + pid));
    const t = META.topics[p.topic - 1];
    const siblings = META.problems.filter(x => x.topic === p.topic);
    const idx = siblings.findIndex(x => x.id === pid);
    const prev = siblings[idx - 1], next = siblings[idx + 1];
    const langs = META.langs;
    let lang = store.get("lang", Object.keys(langs)[0] || "cpp");
    if (!langs[lang]) lang = Object.keys(langs)[0];
    const draftKey = l => `code.${pid}.${l}`;
    app.innerHTML = `<div class="row small muted no-print" style="margin-bottom:10px">
        <a href="#/topic/${t.id}/bai-tap">← ${t.id}. ${esc(t.name)}</a><span class="grow"></span>
        ${prev ? `<a class="btn" href="#/problem/${prev.id}">← ${prev.id}</a>` : ""}${next ? `<a class="btn" href="#/problem/${next.id}">${next.id} →</a>` : ""}</div>
      <div class="prob-layout">
      <article class="panel stmt">
        <div class="row"><span class="mono muted">${p.id}</span>${lvBadge(p.level)}${status(p.id)}</div>
        <h1>${esc(p.title)}</h1>
        <div class="limits">Giới hạn thời gian: ${p.tl / 1000} giây (Python ×3) · Giới hạn bộ nhớ: ${p.ml} MB${p.checker === "float" ? " · Chấp nhận sai số 10⁻⁶" : ""}</div>
        ${MD.render(p.statement)}
        <h3>Dữ liệu vào</h3>${MD.render(p.input)}
        <h3>Kết quả</h3>${MD.render(p.output)}
        ${p.samples.map((s, i) => `<h3>Ví dụ ${i + 1}</h3><div class="sample">
          <div><div class="lbl">Input<button data-copy="${i}">Sao chép</button></div><pre>${esc(s.input)}</pre></div>
          <div><div class="lbl">Output</div><pre>${esc(s.output)}</pre></div></div>`).join("")}
        ${p.note ? `<h3>Ghi chú</h3>${MD.render(p.note)}` : ""}
        <div style="margin-top:12px">${p.tags.map(g => `<a class="tag" href="#/problems" data-tag="${esc(g)}">${esc(g)}</a>`).join("")}</div>
      </article>
      <section class="editor-wrap">
        <div class="panel">
          <div class="row" style="margin-bottom:8px">
            <select id="lang">${Object.entries(langs).map(([k, v]) => `<option value="${k}" ${k === lang ? "selected" : ""}>${esc(v)}</option>`).join("")}</select>
            <button class="btn" id="tplBtn" title="Chèn code mẫu">Code mẫu</button>
            <span class="grow"></span>
            <button class="btn" id="runBtn">▷ Chạy thử</button>
            <button class="btn primary" id="subBtn" title="Ctrl + Enter">Nộp bài</button>
          </div>
          <div class="editor-box"><div class="gutter" id="gutter"></div><textarea class="editor" id="code" spellcheck="false" autocapitalize="off" autocomplete="off"></textarea></div>
          <details style="margin-top:8px"><summary>Chạy với input tự nhập</summary>
            <div class="custom-io"><textarea id="cin" placeholder="Input…">${esc(p.samples[0]?.input || "")}</textarea><textarea id="cout" placeholder="Output…" readonly></textarea></div>
          </details>
          ${p.ready ? "" : `<div class="small muted" id="prepNote" style="margin-top:6px">⏳ Bộ test đang được sinh lần đầu ở nền — lần nộp đầu tiên có thể chờ vài giây.</div>`}
          <div id="result"></div>
        </div>
      </section></div>`;
    const ta = $("#code");
    ta.value = store.get(draftKey(lang), TEMPLATES[lang] || "");
    const sync = setupEditor(ta, $("#gutter"), () => submit());
    ta.addEventListener("input", () => store.set(draftKey(lang), ta.value));
    $("#lang").onchange = e => {
      store.set(draftKey(lang), ta.value); lang = e.target.value; store.set("lang", lang);
      ta.value = store.get(draftKey(lang), TEMPLATES[lang] || ""); sync();
    };
    $("#tplBtn").onclick = () => { if (!ta.value.trim() || confirm("Thay code hiện tại bằng code mẫu?")) { ta.value = TEMPLATES[lang]; sync(); store.set(draftKey(lang), ta.value); } };
    $$("[data-copy]").forEach(b => b.onclick = () => copyText(p.samples[+b.dataset.copy].input, b));
    $$(".stmt .tag").forEach(a => a.onclick = () => { const f = store.get("filters", { topic: "", levels: [], q: "", status: "" }); f.q = a.dataset.tag; f.topic = ""; store.set("filters", f); });
    $("#runBtn").onclick = async () => {
      const btn = $("#runBtn"); btn.disabled = true; $("#cout").value = "Đang chạy…";
      $("details").open = true;
      try {
        const r = await api("/api/run", { lang, code: ta.value, input: $("#cin").value });
        $("#cout").value = r.verdict === "OK" ? r.output : `[${r.verdict}]\n${r.error || ""}`;
        if (r.verdict === "OK") $("#cout").value += `\n\n— ${r.time} ms, ${Math.round(r.mem / 1024)} MB`;
      } catch (e) { $("#cout").value = "Lỗi: " + e.message; }
      btn.disabled = false;
    };
    $("#subBtn").onclick = () => submit();
    async function submit() {
      const btn = $("#subBtn"); if (btn.disabled) return;
      btn.disabled = true; store.set(draftKey(lang), ta.value);
      $("#result").innerHTML = `<div class="verdict wait">Đang chấm…</div>`;
      try {
        const r = await api("/api/submit", { pid, lang, code: ta.value, user });
        markSolved(pid, r.ok);
        $("#prepNote")?.remove();
        $("#result").innerHTML = renderResult(r);
      } catch (e) { $("#result").innerHTML = `<div class="verdict bad">Lỗi: ${esc(e.message)}</div>`; }
      btn.disabled = false;
    }
  }

  function renderResult(r) {
    const ok = r.ok;
    let h = `<div class="verdict ${ok ? "ok" : "bad"}">${ok ? "✓ " : ""}${esc(r.verdict)}${r.time != null && r.tests?.length ? ` · ${r.time} ms · ${Math.round((r.mem || 0) / 1024)} MB` : ""}</div>`;
    if (r.compile) h += `<div class="detail"><b>Thông báo biên dịch</b><pre>${esc(r.compile)}</pre></div>`;
    if (r.tests?.length) {
      h += `<table class="tests"><thead><tr><th>Test</th><th>Kết quả</th><th>Thời gian</th><th>Bộ nhớ</th></tr></thead><tbody>`;
      r.tests.forEach(t => {
        const name = { OK: "OK", WA: "Wrong answer", TLE: "Time limit", MLE: "Memory limit", RE: "Runtime error" }[t.status];
        h += `<tr><td>#${t.test}</td><td class="${t.status === "OK" ? "st-OK" : "st-bad"}">${name}</td><td>${t.time} ms</td><td>${Math.round(t.mem / 1024)} MB</td></tr>`;
      });
      h += `</tbody></table><div class="small muted" style="margin:6px 0">${r.tests.length}/${r.total} test đã chạy${ok ? "" : " — dừng ở test sai đầu tiên (giống Codeforces)"}.</div>`;
      const bad = r.tests.find(t => t.status !== "OK");
      if (bad) {
        h += `<div class="detail"><b>Test #${bad.test}</b>
          <div class="small muted">Input</div><pre>${esc(bad.input)}</pre>
          ${bad.status === "WA" ? `<div class="small muted">Output của bạn</div><pre>${esc(bad.output)}</pre><div class="small muted">Đáp án</div><pre>${esc(bad.answer)}</pre>` : ""}
          ${bad.checker ? `<div class="small muted">Checker / thông báo</div><pre>${esc(bad.checker)}</pre>` : ""}</div>`;
      }
    }
    return h;
  }

  // ------------------------------------------------------------ tổng hợp đề
  function contestPage(arg) {
    setNav("contest");
    const saved = store.get("contest", null);
    if (arg && arg.startsWith("run") && saved) return contestRun(saved);
    const qs = new URLSearchParams((location.hash.split("?")[1]) || "");
    const pre = (qs.get("topics") || "").split(",").filter(Boolean).map(Number);
    const allTags = [...new Set(META.problems.flatMap(p => p.tags))].sort();
    app.innerHTML = `<h1>Tổng hợp đề</h1><p class="muted">Chọn chuyên đề / thẻ kiến thức, mức độ và số bài — công cụ sẽ trộn ngẫu nhiên thành một đề, có thể làm bài tính giờ hoặc in ra giấy.</p>
      <div class="contest-grid"><div class="panel">
        <b>Chuyên đề</b> <span class="small"><a href="#" id="allT">chọn tất cả</a> · <a href="#" id="noneT">bỏ chọn</a></span>
        <div class="topic-checks">${META.topics.map(t => `<label><input type="checkbox" value="${t.id}" ${pre.includes(t.id) ? "checked" : ""}> ${t.id}. ${esc(t.name)}</label>`).join("")}</div>
        <div style="margin-top:10px"><b>Thẻ kiến thức</b> <span class="small muted">(bài có ít nhất một thẻ; bỏ trống = không lọc)</span>
          <input id="tagIn" list="tagList" placeholder="vd: hai con trỏ, BIT, gcd" style="width:100%;margin-top:4px"><datalist id="tagList">${allTags.map(g => `<option value="${esc(g)}">`).join("")}</datalist></div>
        <div class="row" style="margin-top:10px"><label>Mức độ từ <select id="lvA">${[1, 2, 3, 4, 5].map(l => `<option value="${l}">${LV_NAME[l]}</option>`).join("")}</select></label>
          <label>đến <select id="lvB">${[1, 2, 3, 4, 5].map(l => `<option value="${l}" ${l === 4 ? "selected" : ""}>${LV_NAME[l]}</option>`).join("")}</select></label></div>
        <div class="row" style="margin-top:10px"><label>Số bài <input id="cnt" type="number" min="1" max="30" value="6" style="width:70px"></label>
          <label>Thời gian (phút) <input id="dur" type="number" min="5" max="600" value="120" style="width:80px"></label></div>
        <label style="display:block;margin-top:8px"><input type="checkbox" id="unsolved"> Chỉ lấy bài tôi chưa giải</label>
        <label style="display:block"><input type="checkbox" id="spread" checked> Rải đều các chuyên đề, sắp xếp từ dễ đến khó</label>
        <div class="row" style="margin-top:12px"><button class="btn primary" id="gen">Tạo đề</button>
        ${saved ? `<a class="btn" href="#/contest/run">Tiếp tục đề đang làm</a>` : ""}</div>
      </div><div id="genOut" class="panel"><div class="empty">Chưa có đề. Hãy chọn tiêu chí và bấm “Tạo đề”.</div></div></div>`;
    $("#allT").onclick = e => { e.preventDefault(); $$(".topic-checks input").forEach(c => c.checked = true); };
    $("#noneT").onclick = e => { e.preventDefault(); $$(".topic-checks input").forEach(c => c.checked = false); };
    $("#gen").onclick = () => {
      const topics = $$(".topic-checks input:checked").map(c => +c.value);
      const tags = $("#tagIn").value.split(",").map(s => s.trim().toLowerCase()).filter(Boolean);
      const a = +$("#lvA").value, b = +$("#lvB").value, n = +$("#cnt").value;
      let pool = META.problems.filter(p => (!topics.length || topics.includes(p.topic)) && p.level >= Math.min(a, b) && p.level <= Math.max(a, b) &&
        (!tags.length || p.tags.some(g => tags.includes(g.toLowerCase()))) && (!$("#unsolved").checked || !solved.has(p.id)));
      const r = rng(Date.now());
      let picked;
      if ($("#spread").checked) {
        const groups = {}; shuffle(pool, r).forEach(p => (groups[p.topic] = groups[p.topic] || []).push(p));
        const keys = shuffle(Object.keys(groups), r); picked = [];
        for (let round = 0; picked.length < n && keys.some(k => groups[k].length); round++)
          for (const k of keys) if (groups[k].length && picked.length < n) picked.push(groups[k].pop());
        picked.sort((x, y) => x.level - y.level || x.id.localeCompare(y.id));
      } else picked = shuffle(pool, r).slice(0, n);
      if (!picked.length) { $("#genOut").innerHTML = `<div class="empty">Không có bài nào thoả tiêu chí.</div>`; return; }
      const c = { ids: picked.map(p => p.id), duration: +$("#dur").value, created: Date.now(), start: null };
      $("#genOut").innerHTML = `<div class="row"><h3 class="grow" style="margin:0">Đề gồm ${picked.length} bài</h3>
        <button class="btn" id="printBtn">🖨 In đề</button><button class="btn primary" id="startBtn">Bắt đầu làm bài (${c.duration} phút)</button></div>
        <table class="list"><tbody>${picked.map((p, i) => `<tr><td><b>${String.fromCharCode(65 + i)}</b></td><td><a href="#/problem/${p.id}">${esc(p.title)}</a></td>
        <td class="small">${p.topic}. ${esc(META.topics[p.topic - 1].name)}</td><td>${lvBadge(p.level)}</td></tr>`).join("")}</tbody></table>`;
      $("#startBtn").onclick = () => { c.start = Date.now(); store.set("contest", c); location.hash = "#/contest/run"; };
      $("#printBtn").onclick = () => printSet(c.ids);
    };
  }
  async function printSet(ids) {
    app.innerHTML = `<div class="loading">Đang chuẩn bị bản in…</div>`;
    const ps = await Promise.all(ids.map(id => PROB[id] || api("/api/problem/" + id).then(p => (PROB[id] = p))));
    app.innerHTML = `<div class="row no-print"><h1 class="grow">Bản in đề (${ps.length} bài)</h1><button class="btn primary" onclick="window.print()">🖨 In / Lưu PDF</button></div>` +
      ps.map((p, i) => `<article class="panel stmt print-break" style="margin-bottom:16px"><h1>Bài ${String.fromCharCode(65 + i)}. ${esc(p.title)}</h1>
        <div class="limits">Thời gian: ${p.tl / 1000}s · Bộ nhớ: ${p.ml}MB</div>${MD.render(p.statement)}<h3>Dữ liệu vào</h3>${MD.render(p.input)}
        <h3>Kết quả</h3>${MD.render(p.output)}${p.samples.map((s, k) => `<h3>Ví dụ ${k + 1}</h3><div class="sample"><pre>${esc(s.input)}</pre><pre>${esc(s.output)}</pre></div>`).join("")}</article>`).join("");
  }
  async function contestRun(c) {
    const subs = await api("/api/submissions?limit=100000&user=" + encodeURIComponent(user)).catch(() => []);
    const after = subs.filter(s => Date.parse(s.time.replace(" ", "T")) >= c.start - 1000);
    const end = c.start + c.duration * 60000;
    const rows = c.ids.map((id, i) => {
      const mine = after.filter(s => s.pid === id);
      const ac = mine.find(s => s.ok);
      const p = META.problems.find(x => x.id === id);
      return { i, p, tries: mine.length, ac };
    });
    const score = rows.filter(r => r.ac).length;
    app.innerHTML = `<div class="row"><h1 class="grow">Đề đang làm</h1><span class="timer" id="timer"></span>
      <button class="btn" id="endBtn">Kết thúc đề</button></div>
      <div class="panel"><table class="list"><thead><tr><th>Bài</th><th>Tên</th><th>Mức độ</th><th>Số lần nộp</th><th>Kết quả</th></tr></thead><tbody>
      ${rows.map(r => `<tr><td><b>${String.fromCharCode(65 + r.i)}</b></td><td><a href="#/problem/${r.p.id}">${esc(r.p.title)}</a></td><td>${lvBadge(r.p.level)}</td>
      <td>${r.tries}</td><td>${r.ac ? `<span class="solved-mark">✓ ${esc(r.ac.time.slice(11))}</span>` : (r.tries ? '<span style="color:var(--bad)">✗</span>' : "—")}</td></tr>`).join("")}
      </tbody></table><p><b>Điểm: ${score}/${rows.length}</b> <span class="muted small">(chỉ tính bài nộp sau khi bắt đầu đề; bấm vào tên bài để làm, quay lại trang này để xem tổng kết)</span></p></div>`;
    const tick = () => {
      const left = Math.max(0, end - Date.now());
      const el = $("#timer"); if (!el) return clearInterval(iv);
      el.textContent = left ? new Date(left).toISOString().slice(11, 19) : "Hết giờ!";
      el.style.color = left < 5 * 60000 ? "var(--bad)" : "";
    };
    const iv = setInterval(tick, 1000); tick();
    $("#endBtn").onclick = () => { if (confirm("Kết thúc và xoá đề đang làm?")) { store.set("contest", null); location.hash = "#/contest"; } };
  }

  // ------------------------------------------------------------ bài nộp
  async function subsPage() {
    setNav("submissions");
    const all = store.get("subsAll", false);
    const list = await api("/api/submissions?limit=300" + (all ? "" : "&user=" + encodeURIComponent(user)));
    app.innerHTML = `<div class="row"><h1 class="grow">Bài nộp ${all ? "của cả lớp" : "của " + esc(user)}</h1>
      <label class="small"><input type="checkbox" id="allU" ${all ? "checked" : ""}> Xem cả lớp (giáo viên)</label></div>
      <div class="panel" style="padding:6px 8px">${list.length ? `<table class="list"><thead><tr><th>Thời gian</th><th>Người nộp</th><th>Bài</th><th>Ngôn ngữ</th><th>Kết quả</th><th>Thời gian chạy</th><th></th></tr></thead><tbody>
      ${list.map((s, i) => `<tr><td class="small">${esc(s.time)}</td><td>${esc(s.user)}</td><td><a href="#/problem/${s.pid}">${s.pid} — ${esc(s.title)}</a></td>
      <td>${esc(META.langs[s.lang] || s.lang)}</td><td style="color:${s.ok ? "var(--ok)" : "var(--bad)"};font-weight:700">${esc(s.verdict)}</td>
      <td>${s.ms} ms</td><td><button class="btn" data-i="${i}">Xem code</button></td></tr>`).join("")}</tbody></table>` : `<div class="empty">Chưa có bài nộp nào.</div>`}</div>
      <div id="codeView"></div>`;
    $("#allU").onchange = e => { store.set("subsAll", e.target.checked); subsPage(); };
    $$("[data-i]").forEach(b => b.onclick = () => {
      const s = list[+b.dataset.i];
      $("#codeView").innerHTML = `<div class="panel" style="margin-top:14px"><div class="row"><b class="grow">${esc(s.user)} · ${s.pid} · ${esc(s.verdict)}</b>
        <button class="btn" id="cpy">Sao chép</button></div><pre class="code"><code>${esc(s.code)}</code></pre></div>`;
      $("#cpy").onclick = e => copyText(s.code, e.target);
      $("#codeView").scrollIntoView({ behavior: "smooth" });
    });
  }

  // ------------------------------------------------------------ khởi động
  (async function init() {
    try {
      META = await api("/api/meta");
      await syncSolved();
      route();
    } catch (e) {
      app.innerHTML = `<div class="panel">Không kết nối được máy chủ: ${esc(e.message)}.<br>Hãy chạy <code>python3 server.py</code> rồi mở lại trang.</div>`;
    }
  })();
})();
