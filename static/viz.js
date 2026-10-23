// Mô phỏng thuật toán từng bước cho 20 chuyên đề.
// Mỗi mô phỏng: params (ô nhập), build(params) → danh sách khung hình, render(khung) → HTML.
(function () {
  "use strict";
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const nums = s => String(s).split(/[\s,;]+/).filter(Boolean).map(Number).filter(x => !isNaN(x));
  const clone = o => JSON.parse(JSON.stringify(o));

  // ------------------------------------------------------------ khối hiển thị dùng chung
  function cells(vals, cls = () => "", opt = {}) {
    const start = opt.start ?? 0;
    return `<div class="cells ${opt.idx === false ? "" : "withidx"}">` + vals.map((v, i) => {
      const p = opt.ptr && opt.ptr[i];
      return `<div class="cell ${cls(i) || ""}">${esc(v)}${opt.idx === false ? "" : `<span class="idx">${i + start}</span>`}${p ? `<span class="ptr">${esc(p)}</span>` : ""}</div>`;
    }).join("") + `</div>`;
  }
  function table(data, opt = {}) {
    let h = `<table class="vtable">`;
    if (opt.colHead) h += `<tr><th></th>${opt.colHead.map(c => `<th>${esc(c)}</th>`).join("")}</tr>`;
    data.forEach((row, i) => {
      h += `<tr>${opt.rowHead ? `<th>${esc(opt.rowHead[i])}</th>` : ""}${row.map((v, j) => `<td class="${opt.cls ? opt.cls(i, j) || "" : ""}">${esc(v)}</td>`).join("")}</tr>`;
    });
    return h + `</table>`;
  }
  function graph(nodes, edges, opt = {}) {
    const W = opt.w || 620, H = opt.h || 320, R = opt.r || 18;
    const byId = {}; nodes.forEach(n => byId[n.id] = n);
    let s = `<svg class="g" viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px">`;
    if (opt.directed) s += `<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/></marker></defs>`;
    edges.forEach(e => {
      const a = byId[e.u], b = byId[e.v]; if (!a || !b) return;
      const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
      const x1 = a.x + dx / L * R, y1 = a.y + dy / L * R, x2 = b.x - dx / L * (R + (opt.directed ? 2 : 0)), y2 = b.y - dy / L * (R + (opt.directed ? 2 : 0));
      s += `<g class="ed ${e.cls || ""}"><line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" ${opt.directed ? 'marker-end="url(#arr)"' : ""}/>`;
      if (e.label != null) s += `<text x="${(a.x + b.x) / 2 + 6}" y="${(a.y + b.y) / 2 - 6}">${esc(e.label)}</text>`;
      s += `</g>`;
    });
    nodes.forEach(n => {
      s += `<g class="nd ${n.cls || ""}"><circle cx="${n.x}" cy="${n.y}" r="${R}"/><text x="${n.x}" y="${n.y + 4}" text-anchor="middle">${esc(n.label ?? n.id)}</text>`;
      if (n.sub != null) s += `<text class="sub" x="${n.x}" y="${n.y + R + 14}" text-anchor="middle">${esc(n.sub)}</text>`;
      s += `</g>`;
    });
    return s + `</svg>`;
  }
  function treePos(children, root, W = 620, H = 300) {
    const pos = {}; let leaf = 0; const depth = {};
    (function dfs(u, d) {
      depth[u] = d;
      const ch = children[u] || [];
      if (!ch.length) { pos[u] = { x: leaf++, d }; return; }
      ch.forEach(v => dfs(v, d + 1));
      pos[u] = { x: (pos[ch[0]].x + pos[ch[ch.length - 1]].x) / 2, d };
    })(root, 0);
    const maxD = Math.max(...Object.values(depth)), nl = Math.max(1, leaf - 1);
    for (const k in pos) pos[k] = { x: 40 + (W - 80) * (leaf === 1 ? .5 : pos[k].x / nl), y: 30 + (H - 70) * (maxD ? pos[k].d / maxD : 0) };
    return pos;
  }
  const kv = obj => `<div class="kv">${Object.entries(obj).map(([k, v]) => `<span>${esc(k)}: <b>${esc(v)}</b></span>`).join("")}</div>`;

  // ------------------------------------------------------------ đồ thị mẫu
  const G_POS = { 1: [60, 160], 2: [180, 60], 3: [180, 260], 4: [310, 160], 5: [440, 60], 6: [440, 260], 7: [560, 160], 8: [310, 290] };
  const G_W = [[1, 2, 4], [1, 3, 2], [2, 3, 1], [2, 4, 5], [3, 4, 8], [3, 8, 3], [8, 6, 2], [4, 6, 6], [4, 5, 2], [5, 7, 3], [6, 7, 1], [5, 6, 4]];
  const gNodes = (f) => Object.entries(G_POS).map(([id, [x, y]]) => Object.assign({ id: +id, x, y }, f ? f(+id) : {}));

  const DEFS = {};

  // 1. Sàng Eratosthenes ------------------------------------------------
  DEFS.sieve = {
    title: "Sàng Eratosthenes", params: [{ id: "n", label: "n", value: 60 }],
    build(p) {
      const n = Math.max(2, Math.min(150, +p.n || 60)); const st = Array(n + 1).fill(0); // 0 chưa rõ, 1 nguyên tố, 2 hợp số
      const fr = []; const push = (cap, cur, hl) => fr.push({ st: st.slice(), cur, hl, cap, n });
      push("Ban đầu coi mọi số từ 2 đến n là nguyên tố (chưa bị gạch).", -1, -1);
      for (let i = 2; i <= n; i++) {
        if (st[i] === 2) continue;
        st[i] = 1;
        if (i * i > n) { push(`${i}² = ${i * i} > ${n}: mọi số chưa bị gạch còn lại đều là số nguyên tố.`, i, -1); for (let k = i; k <= n; k++) if (!st[k]) st[k] = 1; push("Hoàn tất! Các ô xanh là số nguyên tố.", -1, -1); break; }
        push(`${i} chưa bị gạch ⇒ ${i} là số nguyên tố. Bắt đầu gạch các bội từ ${i}×${i} = ${i * i}.`, i, -1);
        for (let j = i * i; j <= n; j += i) { const was = st[j]; st[j] = 2; push(`Gạch ${j} = ${i} × ${j / i}${was === 2 ? " (đã bị gạch trước đó)" : ""}.`, i, j); }
      }
      return fr;
    },
    render(f) {
      const vals = []; for (let i = 1; i <= f.n; i++) vals.push(i);
      return cells(vals, i => { const x = i + 1; if (x === f.hl) return "bad"; if (x === f.cur) return "cur"; if (x === 1) return "dim"; return f.st[x] === 1 ? "prime" : f.st[x] === 2 ? "off" : ""; }, { idx: false })
        + kv({ "số nguyên tố": f.st.filter(v => v === 1).length });
    },
  };

  // 2. Tổng tiền tố -----------------------------------------------------
  DEFS.prefix = {
    title: "Mảng cộng dồn", params: [{ id: "a", label: "Dãy a", value: "3 1 4 1 5 9 2 6" }, { id: "q", label: "Truy vấn l r", value: "3 6" }],
    build(p) {
      const a = nums(p.a).slice(0, 16); const [l, r] = nums(p.q); const n = a.length; const pre = [0];
      const fr = [{ a, pre: [0], cap: "p[0] = 0. Ta sẽ tính p[i] = p[i-1] + a[i].", hi: -1 }];
      for (let i = 1; i <= n; i++) { pre.push(pre[i - 1] + a[i - 1]); fr.push({ a, pre: pre.slice(), hi: i, cap: `p[${i}] = p[${i - 1}] + a[${i}] = ${pre[i - 1]} + ${a[i - 1]} = ${pre[i]}` }); }
      if (l >= 1 && r <= n && l <= r) {
        fr.push({ a, pre: pre.slice(), q: [l, r], cap: `Tổng a[${l}..${r}] = p[${r}] − p[${l - 1}] = ${pre[r]} − ${pre[l - 1]} = ${pre[r] - pre[l - 1]} — chỉ một phép trừ!` });
      }
      return fr;
    },
    render(f) {
      const q = f.q || [];
      return `<div class="muted small">Dãy a (đánh số từ 1)</div>` + cells(f.a, i => q.length && i + 1 >= q[0] && i + 1 <= q[1] ? "hl" : (i + 1 === f.hi ? "cur" : ""), { start: 1 }) +
        `<div class="muted small">Mảng cộng dồn p</div>` + cells(f.pre, i => q.length && (i === q[1] || i === q[0] - 1) ? "on" : (i === f.hi ? "cur" : (i === f.hi - 1 ? "hl" : "")));
    },
  };

  // 3. Tìm kiếm nhị phân -------------------------------------------------
  DEFS.bsearch = {
    title: "Tìm kiếm nhị phân", params: [{ id: "a", label: "Dãy tăng", value: "2 5 8 12 16 23 38 56 72 91" }, { id: "x", label: "Tìm x", value: 23 }],
    build(p) {
      const a = nums(p.a).sort((x, y) => x - y).slice(0, 20); const x = +p.x; const fr = [];
      let lo = 0, hi = a.length - 1, step = 0;
      fr.push({ a, lo, hi, mid: -1, cap: `Tìm ${x} trong dãy đã sắp xếp. Đoạn tìm kiếm ban đầu [${lo}, ${hi}].` });
      while (lo <= hi) {
        const mid = (lo + hi) >> 1; step++;
        if (a[mid] === x) { fr.push({ a, lo, hi, mid, found: mid, cap: `Bước ${step}: mid = ${mid}, a[mid] = ${a[mid]} = x. Tìm thấy tại vị trí ${mid}!` }); return fr; }
        if (a[mid] < x) { fr.push({ a, lo, hi, mid, cap: `Bước ${step}: mid = ${mid}, a[mid] = ${a[mid]} < ${x} ⇒ bỏ nửa trái, lo = ${mid + 1}.` }); lo = mid + 1; }
        else { fr.push({ a, lo, hi, mid, cap: `Bước ${step}: mid = ${mid}, a[mid] = ${a[mid]} > ${x} ⇒ bỏ nửa phải, hi = ${mid - 1}.` }); hi = mid - 1; }
      }
      fr.push({ a, lo, hi, mid: -1, cap: `lo > hi: không có ${x} trong dãy (sau ${step} bước, so với ${a.length} bước nếu tìm tuần tự).` });
      return fr;
    },
    render(f) {
      const ptr = {}; if (f.lo >= 0 && f.lo < f.a.length) ptr[f.lo] = "lo"; if (f.hi >= 0 && f.hi < f.a.length) ptr[f.hi] = (ptr[f.hi] ? ptr[f.hi] + "," : "") + "hi";
      if (f.mid >= 0) ptr[f.mid] = (ptr[f.mid] ? ptr[f.mid] + "," : "") + "mid";
      return cells(f.a, i => i === f.found ? "on" : i === f.mid ? "cur" : (i < f.lo || i > f.hi ? "off" : "hl"), { ptr });
    },
  };

  // 4. Hai con trỏ ----------------------------------------------------------
  DEFS.twopointers = {
    title: "Hai con trỏ: đoạn dài nhất có tổng ≤ s", params: [{ id: "a", label: "Dãy dương", value: "2 6 4 3 6 8 9 1 2" }, { id: "s", label: "s", value: 15 }],
    build(p) {
      const a = nums(p.a).slice(0, 18); const s = +p.s; const fr = []; let l = 0, sum = 0, best = 0, bl = 0, br = -1;
      for (let r = 0; r < a.length; r++) {
        sum += a[r]; fr.push({ a, l, r, sum, best, bl, br, cap: `Mở rộng phải: thêm a[${r}] = ${a[r]}, tổng = ${sum}.` });
        while (sum > s) { sum -= a[l]; fr.push({ a, l: l + 1, r, sum, best, bl, br, cap: `Tổng > ${s} ⇒ thu hẹp trái: bỏ a[${l}] = ${a[l]}, tổng = ${sum}.` }); l++; }
        if (r - l + 1 > best) { best = r - l + 1; bl = l; br = r; fr.push({ a, l, r, sum, best, bl, br, cap: `Đoạn [${l}, ${r}] dài ${best} — tốt nhất hiện tại.` }); }
      }
      fr.push({ a, l: -1, r: -1, sum, best, bl, br, cap: `Xong. Mỗi con trỏ chỉ đi tiến nên tổng số bước O(n). Đáp án: ${best}.` });
      return fr;
    },
    render(f) {
      const ptr = {}; if (f.l >= 0) ptr[f.l] = "l"; if (f.r >= 0) ptr[f.r] = (ptr[f.r] ? "l,r" : "r");
      return cells(f.a, i => f.l >= 0 && i >= f.l && i <= f.r ? "cur" : (i >= f.bl && i <= f.br ? "on" : ""), { ptr }) + kv({ "tổng cửa sổ": f.sum, "tốt nhất": f.best });
    },
  };

  // 5. Heap -----------------------------------------------------------------
  DEFS.heap = {
    title: "Min-heap: thêm và lấy phần tử nhỏ nhất", params: [{ id: "a", label: "Các số thêm vào", value: "7 3 9 1 5 8 2" }, { id: "k", label: "Số lần pop", value: 3 }],
    build(p) {
      const xs = nums(p.a).slice(0, 15), k = Math.min(+p.k || 0, xs.length); const h = []; const fr = [];
      const push = (cap, hl = [], out) => fr.push({ h: h.slice(), hl, cap, out });
      for (const x of xs) {
        h.push(x); let i = h.length - 1; push(`Thêm ${x} vào cuối mảng (vị trí ${i}).`, [i]);
        while (i > 0) {
          const pr = (i - 1) >> 1;
          if (h[pr] <= h[i]) { push(`Cha ${h[pr]} ≤ ${h[i]}: dừng vun đống lên.`, [i, pr]); break; }
          [h[pr], h[i]] = [h[i], h[pr]]; push(`Cha lớn hơn ⇒ đổi chỗ, ${h[pr]} đi lên vị trí ${pr}.`, [pr, i]); i = pr;
        }
      }
      const outs = [];
      for (let t = 0; t < k; t++) {
        const top = h[0]; outs.push(top); h[0] = h[h.length - 1]; h.pop();
        push(`Pop: lấy đỉnh ${top} (nhỏ nhất), đưa phần tử cuối lên gốc.`, [0], outs.slice());
        let i = 0;
        while (true) {
          const l = 2 * i + 1, r = l + 1; let m = i;
          if (l < h.length && h[l] < h[m]) m = l; if (r < h.length && h[r] < h[m]) m = r;
          if (m === i) { push("Đã đúng thứ tự heap.", [i], outs.slice()); break; }
          [h[m], h[i]] = [h[i], h[m]]; push(`Đổi với con nhỏ hơn: ${h[i]} lên vị trí ${i}.`, [i, m], outs.slice()); i = m;
        }
      }
      return fr;
    },
    render(f) {
      const ch = {}; f.h.forEach((_, i) => { if (i) (ch[(i - 1) >> 1] = ch[(i - 1) >> 1] || []).push(i); });
      let s = "";
      if (f.h.length) {
        const pos = treePos(ch, 0, 620, 240);
        s = graph(f.h.map((v, i) => ({ id: i, x: pos[i].x, y: pos[i].y, label: v, cls: f.hl.includes(i) ? "hl" : "", sub: i })),
          f.h.slice(1).map((_, j) => ({ u: (j) >> 1, v: j + 1 })), { h: 260 });
      }
      return s + `<div class="muted small">Mảng lưu heap (con của i là 2i+1, 2i+2)</div>` + cells(f.h, i => f.hl.includes(i) ? "hl" : "") +
        (f.out ? kv({ "đã lấy ra": f.out.join(" ") }) : "");
    },
  };

  // 6. N quân hậu -----------------------------------------------------------
  DEFS.nqueens = {
    title: "Quay lui: N quân hậu", params: [{ id: "n", label: "n (4..8)", value: 5 }],
    build(p) {
      const n = Math.max(4, Math.min(8, +p.n || 5)); const q = Array(n).fill(-1); const fr = []; let done = false;
      const ok = (r, c) => { for (let i = 0; i < r; i++) if (q[i] === c || Math.abs(q[i] - c) === r - i) return false; return true; };
      (function go(r) {
        if (done || fr.length > 400) return;
        if (r === n) { fr.push({ n, q: q.slice(), cap: "Đặt đủ " + n + " quân hậu — tìm được một nghiệm!", sol: true }); done = true; return; }
        for (let c = 0; c < n && !done; c++) {
          if (ok(r, c)) { q[r] = c; fr.push({ n, q: q.slice(), cur: [r, c], cap: `Hàng ${r + 1}: đặt hậu ở cột ${c + 1}.` }); go(r + 1); if (!done) { fr.push({ n, q: q.slice(), cur: [r, c], back: true, cap: `Không đặt tiếp được ⇒ quay lui, bỏ hậu ở (${r + 1}, ${c + 1}).` }); q[r] = -1; } }
          else fr.push({ n, q: q.slice(), bad: [r, c], cap: `Ô (${r + 1}, ${c + 1}) bị khống chế — thử cột tiếp theo.` });
        }
      })(0);
      return fr;
    },
    render(f) {
      let s = `<div class="board" style="grid-template-columns:repeat(${f.n},40px)">`;
      for (let r = 0; r < f.n; r++) for (let c = 0; c < f.n; c++) {
        const isQ = f.q[r] === c; const bad = f.bad && f.bad[0] === r && f.bad[1] === c;
        s += `<div class="${(r + c) % 2 ? "b" : "w"} ${bad ? "att" : ""} ${isQ ? "q" : ""}">${isQ ? "♛" : bad ? "✕" : ""}</div>`;
      }
      return s + `</div>`;
    },
  };

  // 7. QHĐ đổi tiền ----------------------------------------------------------
  DEFS.dpcoins = {
    title: "QHĐ: đổi tiền ít đồng xu nhất", params: [{ id: "c", label: "Mệnh giá", value: "1 3 4" }, { id: "x", label: "x", value: 10 }],
    build(p) {
      const c = nums(p.c).filter(v => v > 0).slice(0, 6), x = Math.min(30, +p.x || 10); const INF = "∞"; const dp = [0]; const fr = [];
      fr.push({ dp: [0], cur: 0, cap: "dp[0] = 0 (không cần đồng nào để tạo tổng 0).", from: -1 });
      for (let v = 1; v <= x; v++) {
        let best = Infinity, from = -1;
        for (const ci of c) if (ci <= v && dp[v - ci] !== INF && dp[v - ci] + 1 < best) { best = dp[v - ci] + 1; from = v - ci; }
        dp.push(best === Infinity ? INF : best);
        fr.push({ dp: dp.slice(), cur: v, from, cap: best === Infinity ? `dp[${v}] = ∞ (không tạo được).` : `dp[${v}] = dp[${from}] + 1 = ${best} (dùng đồng ${v - from}). Thử mọi mệnh giá, lấy nhỏ nhất.` });
      }
      return fr;
    },
    render(f) { return cells(f.dp, i => i === f.cur ? "cur" : i === f.from ? "hl" : ""); },
  };

  // 8. QHĐ đếm trên lưới ------------------------------------------------------
  DEFS.dpgrid = {
    title: "QHĐ đếm: số đường đi trên lưới", params: [{ id: "g", label: "Lưới (# là ô cấm, / xuống dòng)", value: "....#/.#.../...#./#...." }],
    build(p) {
      const g = String(p.g).split("/").map(r => r.trim()).filter(Boolean).slice(0, 8); const n = g.length, m = Math.max(...g.map(r => r.length));
      const dp = g.map(r => Array(m).fill("")); const fr = [];
      for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) {
        if ((g[i][j] || "#") === "#") { dp[i][j] = "#"; fr.push({ g, dp: clone(dp), cur: [i, j], cap: `Ô (${i + 1}, ${j + 1}) bị cấm ⇒ 0 đường.` }); continue; }
        const up = i ? (dp[i - 1][j] === "#" ? 0 : dp[i - 1][j]) : 0, lf = j ? (dp[i][j - 1] === "#" ? 0 : dp[i][j - 1]) : 0;
        dp[i][j] = i === 0 && j === 0 ? 1 : up + lf;
        fr.push({ g, dp: clone(dp), cur: [i, j], cap: i === 0 && j === 0 ? "Ô xuất phát: 1 cách." : `dp = trên (${up}) + trái (${lf}) = ${dp[i][j]}` });
      }
      return fr;
    },
    render(f) {
      return table(f.dp, { cls: (i, j) => f.dp[i][j] === "#" ? "bad" : (f.cur[0] === i && f.cur[1] === j ? "cur" : ((f.cur[0] === i + 1 && f.cur[1] === j) || (f.cur[0] === i && f.cur[1] === j + 1) ? "hl" : "")) });
    },
  };

  // 9. LCS --------------------------------------------------------------------
  DEFS.lcs = {
    title: "QHĐ: xâu con chung dài nhất (LCS)", params: [{ id: "a", label: "Xâu a", value: "ABCBDAB" }, { id: "b", label: "Xâu b", value: "BDCABA" }],
    build(p) {
      const a = String(p.a).slice(0, 10), b = String(p.b).slice(0, 10); const n = a.length, m = b.length;
      const dp = Array.from({ length: n + 1 }, () => Array(m + 1).fill(0)); const fr = [];
      for (let i = 1; i <= n; i++) for (let j = 1; j <= m; j++) {
        const eq = a[i - 1] === b[j - 1];
        dp[i][j] = eq ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]);
        fr.push({ a, b, dp: clone(dp), cur: [i, j], eq, cap: eq ? `a[${i}] = b[${j}] = '${a[i - 1]}' ⇒ dp = chéo + 1 = ${dp[i][j]}` : `'${a[i - 1]}' ≠ '${b[j - 1]}' ⇒ dp = max(trên, trái) = ${dp[i][j]}` });
      }
      // truy vết
      let i = n, j = m; const path = []; let s = "";
      while (i && j) { path.push([i, j]); if (a[i - 1] === b[j - 1]) { s = a[i - 1] + s; i--; j--; } else if (dp[i - 1][j] >= dp[i][j - 1]) i--; else j--; }
      fr.push({ a, b, dp: clone(dp), cur: [-1, -1], path, cap: `Truy vết từ góc dưới phải: LCS = "${s}" (độ dài ${dp[n][m]}).` });
      return fr;
    },
    render(f) {
      const onPath = (i, j) => f.path && f.path.some(([x, y]) => x === i && y === j);
      return table(f.dp, {
        colHead: ["∅", ...f.b], rowHead: ["∅", ...f.a],
        cls: (i, j) => onPath(i, j) ? "on" : (i === f.cur[0] && j === f.cur[1] ? "cur" : ((f.eq && i === f.cur[0] - 1 && j === f.cur[1] - 1) || (!f.eq && ((i === f.cur[0] - 1 && j === f.cur[1]) || (i === f.cur[0] && j === f.cur[1] - 1))) ? "hl" : "")),
      });
    },
  };

  // 10. BFS / DFS trên lưới ---------------------------------------------------
  DEFS.bfs = {
    title: "BFS / DFS trên lưới", params: [{ id: "g", label: "Lưới (S xuất phát, # tường, / xuống dòng)", value: "S...#..../.##.#.##./....#..../.#....#../.#.##.#.." }, { id: "mode", label: "BFS hoặc DFS", value: "BFS" }],
    build(p) {
      const g = String(p.g).split("/").filter(Boolean).slice(0, 10).map(r => r.slice(0, 16)); const n = g.length, m = Math.max(...g.map(r => r.length));
      let s = [0, 0]; g.forEach((r, i) => { const j = r.indexOf("S"); if (j >= 0) s = [i, j]; });
      const d = g.map(() => Array(m).fill(-1)); const fr = []; const dfs = String(p.mode).toUpperCase() === "DFS";
      const cont = [s]; d[s[0]][s[1]] = 0; let order = 0; const ord = g.map(() => Array(m).fill(""));
      fr.push({ g, d: clone(d), ord: clone(ord), cur: s, cap: `Bắt đầu ${dfs ? "DFS (ngăn xếp)" : "BFS (hàng đợi)"} từ S.`, dfs });
      while (cont.length) {
        const [x, y] = dfs ? cont.pop() : cont.shift();
        ord[x][y] = ++order;
        const added = [];
        for (const [dx, dy] of [[1, 0], [0, 1], [-1, 0], [0, -1]]) {
          const a = x + dx, b = y + dy;
          if (a >= 0 && b >= 0 && a < n && b < m && (g[a][b] || "#") !== "#" && d[a][b] < 0) { d[a][b] = d[x][y] + 1; cont.push([a, b]); added.push([a, b]); }
        }
        fr.push({ g, d: clone(d), ord: clone(ord), cur: [x, y], added, cap: `Lấy ô (${x}, ${y}) ra (thứ tự thăm ${order}). Đẩy ${added.length} ô kề chưa thăm vào ${dfs ? "ngăn xếp" : "hàng đợi"}.`, dfs });
      }
      fr.push({ g, d: clone(d), ord: clone(ord), cur: [-1, -1], cap: dfs ? "DFS đi sâu theo một hướng trước — số trong ô là thứ tự thăm, không phải khoảng cách ngắn nhất." : "BFS loang theo từng lớp — số trong ô là khoảng cách ngắn nhất từ S.", dfs });
      return fr;
    },
    render(f) {
      const data = f.g.map((r, i) => Array.from({ length: Math.max(...f.g.map(x => x.length)) }, (_, j) => (r[j] || "#") === "#" ? "#" : (f.dfs ? f.ord[i][j] : (f.d[i][j] >= 0 ? f.d[i][j] : ""))));
      return table(data, { cls: (i, j) => data[i][j] === "#" ? "bad" : (f.cur[0] === i && f.cur[1] === j ? "cur" : (f.added && f.added.some(([a, b]) => a === i && b === j) ? "hl" : (f.ord[i][j] ? "on" : (f.d[i][j] >= 0 ? "hl" : "")))) });
    },
  };

  // 11. Cầu và khớp -----------------------------------------------------------
  DEFS.bridges = {
    title: "Tarjan: tìm cầu và đỉnh khớp", params: [],
    build() {
      const E = [[1, 2], [2, 3], [3, 1], [3, 4], [4, 5], [5, 8], [8, 4], [8, 6], [6, 7]];
      const adj = {}; for (let i = 1; i <= 8; i++) adj[i] = []; E.forEach(([a, b], k) => { adj[a].push([b, k]); adj[b].push([a, k]); });
      const tin = {}, low = {}; let t = 0; const fr = []; const bridges = new Set(), cut = new Set(); const tree = new Set();
      const snap = (cap, cur) => fr.push({ tin: { ...tin }, low: { ...low }, cur, cap, bridges: [...bridges], cut: [...cut], tree: [...tree], E });
      (function dfs(u, pe) {
        tin[u] = low[u] = ++t; snap(`Thăm đỉnh ${u}: tin = low = ${t}.`, u); let child = 0;
        for (const [v, k] of adj[u]) {
          if (k === pe) continue;
          if (tin[v]) { if (tin[v] < low[u]) { low[u] = tin[v]; snap(`Cạnh ngược ${u}–${v}: low[${u}] = tin[${v}] = ${tin[v]}.`, u); } }
          else {
            tree.add(k); child++; dfs(v, k); low[u] = Math.min(low[u], low[v]);
            if (low[v] > tin[u]) { bridges.add(k); snap(`low[${v}] = ${low[v]} > tin[${u}] = ${tin[u]} ⇒ cạnh ${u}–${v} là CẦU.`, u); }
            else snap(`Quay về ${u}: low[${u}] = min(low[${u}], low[${v}]) = ${low[u]}.`, u);
            if (pe !== -1 && low[v] >= tin[u] && !cut.has(u)) { cut.add(u); snap(`low[${v}] ≥ tin[${u}] ⇒ ${u} là ĐỈNH KHỚP.`, u); }
          }
        }
        if (pe === -1 && child >= 2) { cut.add(u); snap(`Gốc ${u} có ${child} con trong cây DFS ⇒ là khớp.`, u); }
      })(1, -1);
      snap("Xong: cạnh đỏ là cầu, đỉnh đỏ là khớp.", -1);
      return fr;
    },
    render(f) {
      const P = { 1: [70, 80], 2: [70, 250], 3: [200, 165], 4: [340, 165], 5: [440, 60], 8: [440, 270], 6: [560, 270], 7: [600, 140] };
      const nodes = Object.keys(P).map(k => ({ id: +k, x: P[k][0], y: P[k][1], cls: f.cut.includes(+k) ? "bad" : (+k === f.cur ? "cur" : (f.tin[k] ? "on" : "")), sub: f.tin[k] ? `${f.tin[k]}/${f.low[k]}` : "" }));
      const edges = f.E.map(([u, v], k) => ({ u, v, cls: f.bridges.includes(k) ? "bad" : (f.tree.includes(k) ? "on" : "") }));
      return graph(nodes, edges, { h: 320 }) + `<div class="small muted">Số dưới đỉnh: tin/low. Cạnh xanh: cạnh cây DFS.</div>`;
    },
  };

  // 12. Sắp xếp topo ----------------------------------------------------------
  DEFS.topo = {
    title: "Sắp xếp topo (Kahn)", params: [],
    build() {
      const E = [[1, 3], [2, 3], [2, 4], [3, 5], [4, 5], [4, 7], [5, 6], [7, 6], [1, 8], [8, 6]];
      const indeg = {}; for (let i = 1; i <= 8; i++) indeg[i] = 0; E.forEach(([, b]) => indeg[b]++);
      const q = Object.keys(indeg).filter(k => !indeg[k]).map(Number); const order = []; const fr = [];
      const snap = (cap, cur, used) => fr.push({ indeg: { ...indeg }, q: q.slice(), order: order.slice(), cur, cap, E, used: used || [] });
      snap(`Đưa các đỉnh có bậc vào 0 (${q.join(", ")}) vào hàng đợi.`, -1);
      while (q.length) {
        const u = q.shift(); order.push(u); const used = [];
        E.forEach(([a, b], k) => { if (a === u) { indeg[b]--; used.push(k); if (!indeg[b]) q.push(b); } });
        snap(`Lấy ${u} ra, thêm vào thứ tự topo; giảm bậc vào của các đỉnh nó trỏ tới.`, u, used);
      }
      snap("Hoàn tất: mọi cung đều đi từ trái sang phải trong thứ tự topo.", -1);
      return fr;
    },
    render(f) {
      const P = { 1: [70, 70], 2: [70, 250], 3: [210, 120], 4: [210, 260], 5: [350, 180], 7: [350, 290], 6: [520, 200], 8: [350, 50] };
      const nodes = Object.keys(P).map(k => ({ id: +k, x: P[k][0], y: P[k][1], sub: "vào: " + f.indeg[k], cls: +k === f.cur ? "cur" : (f.order.includes(+k) ? "on" : (f.q.includes(+k) ? "hl" : "")) }));
      return graph(nodes, f.E.map(([u, v], k) => ({ u, v, cls: f.used.includes(k) ? "hl" : (f.order.includes(u) ? "dim" : "") })), { directed: true, h: 330 }) +
        kv({ "hàng đợi": f.q.join(" ") || "∅", "thứ tự topo": f.order.join(" → ") || "∅" });
    },
  };

  // 13. Dijkstra ---------------------------------------------------------------
  DEFS.dijkstra = {
    title: "Dijkstra", params: [{ id: "s", label: "Đỉnh nguồn", value: 1 }],
    build(p) {
      const s = Math.max(1, Math.min(8, +p.s || 1)); const adj = {}; for (let i = 1; i <= 8; i++) adj[i] = [];
      G_W.forEach(([a, b, w], k) => { adj[a].push([b, w, k]); adj[b].push([a, w, k]); });
      const d = {}; for (let i = 1; i <= 8; i++) d[i] = Infinity; d[s] = 0; const done = new Set(); const par = {}; const fr = []; let pq = [[0, s]];
      const snap = (cap, cur, relax) => fr.push({ d: { ...d }, done: [...done], cur, cap, pq: pq.map(x => x.slice()).sort((a, b) => a[0] - b[0]), par: { ...par }, relax: relax || [] });
      snap(`d[${s}] = 0, các đỉnh khác = ∞. Hàng đợi ưu tiên: (0, ${s}).`, -1);
      while (pq.length) {
        pq.sort((a, b) => a[0] - b[0]); const [du, u] = pq.shift();
        if (done.has(u)) { snap(`Lấy (${du}, ${u}) nhưng ${u} đã chốt ⇒ bỏ qua.`, u); continue; }
        done.add(u); const relax = [];
        for (const [v, w, k] of adj[u]) if (!done.has(v) && du + w < d[v]) { d[v] = du + w; par[v] = k; pq.push([d[v], v]); relax.push(k); }
        snap(`Chốt đỉnh ${u} với d = ${du}. Nới lỏng ${relax.length} cạnh.`, u, relax);
      }
      snap("Xong. Cạnh xanh tạo thành cây đường đi ngắn nhất.", -1);
      return fr;
    },
    render(f) {
      const tree = Object.values(f.par);
      const nodes = gNodes(id => ({ cls: id === f.cur ? "cur" : (f.done.includes(id) ? "on" : (f.d[id] < Infinity ? "hl" : "")), sub: f.d[id] === Infinity ? "∞" : f.d[id] }));
      return graph(nodes, G_W.map(([u, v, w], k) => ({ u, v, label: w, cls: f.relax.includes(k) ? "hl" : (tree.includes(k) ? "on" : "") }))) +
        kv({ "heap (d, đỉnh)": f.pq.map(([a, b]) => `(${a},${b})`).join(" ") || "∅" });
    },
  };

  // 14. Deque cửa sổ trượt ------------------------------------------------------
  DEFS.deque = {
    title: "Deque đơn điệu: max trên cửa sổ trượt", params: [{ id: "a", label: "Dãy", value: "1 3 -1 -3 5 3 6 7" }, { id: "k", label: "k", value: 3 }],
    build(p) {
      const a = nums(p.a).slice(0, 16), k = Math.max(1, Math.min(a.length, +p.k || 3)); const dq = []; const out = []; const fr = [];
      for (let i = 0; i < a.length; i++) {
        while (dq.length && a[dq[dq.length - 1]] <= a[i]) { const j = dq.pop(); fr.push({ a, dq: dq.slice(), i, k, out: out.slice(), cap: `a[${j}] = ${a[j]} ≤ a[${i}] = ${a[i]} ⇒ bỏ ${j} khỏi cuối deque (không bao giờ là max nữa).` }); }
        dq.push(i); fr.push({ a, dq: dq.slice(), i, k, out: out.slice(), cap: `Thêm chỉ số ${i} vào cuối deque.` });
        if (dq[0] <= i - k) { const j = dq.shift(); fr.push({ a, dq: dq.slice(), i, k, out: out.slice(), cap: `Chỉ số ${j} đã ra khỏi cửa sổ ⇒ bỏ khỏi đầu deque.` }); }
        if (i >= k - 1) { out.push(a[dq[0]]); fr.push({ a, dq: dq.slice(), i, k, out: out.slice(), cap: `Cửa sổ [${i - k + 1}, ${i}]: max = a[${dq[0]}] = ${a[dq[0]]} (đầu deque).` }); }
      }
      return fr;
    },
    render(f) {
      return cells(f.a, i => f.dq.includes(i) ? (i === f.dq[0] ? "on" : "hl") : (i > f.i - f.k && i <= f.i ? "cur" : ""), { ptr: { [f.i]: "i" } }) +
        `<div class="muted small">Deque (chỉ số → giá trị)</div>` + cells(f.dq.map(j => `${j}:${f.a[j]}`), () => "hl", { idx: false }) + kv({ "kết quả": f.out.join(" ") });
    },
  };

  // 15. Sparse table ---------------------------------------------------------------
  DEFS.sparse = {
    title: "Sparse table (min)", params: [{ id: "a", label: "Dãy", value: "5 2 4 7 6 3 1 2" }, { id: "q", label: "Truy vấn l r", value: "1 6" }],
    build(p) {
      const a = nums(p.a).slice(0, 16); const n = a.length; const st = [a.slice()]; const fr = [];
      fr.push({ st: clone(st), a, cap: "Hàng 0: st[0][i] = a[i] (đoạn dài 1).", hj: 0 });
      for (let j = 1; (1 << j) <= n; j++) {
        const row = []; for (let i = 0; i + (1 << j) <= n; i++) row.push(Math.min(st[j - 1][i], st[j - 1][i + (1 << (j - 1))]));
        st.push(row); fr.push({ st: clone(st), a, hj: j, cap: `Hàng ${j}: st[${j}][i] = min(st[${j - 1}][i], st[${j - 1}][i + ${1 << (j - 1)}]) — đoạn dài ${1 << j}.` });
      }
      const [l, r] = nums(p.q);
      if (l >= 0 && r < n && l <= r) {
        const k = Math.floor(Math.log2(r - l + 1));
        fr.push({ st: clone(st), a, q: [l, r, k], cap: `Truy vấn [${l}, ${r}]: k = ⌊log2(${r - l + 1})⌋ = ${k}. min(st[${k}][${l}], st[${k}][${r - (1 << k) + 1}]) = min(${st[k][l]}, ${st[k][r - (1 << k) + 1]}) = ${Math.min(st[k][l], st[k][r - (1 << k) + 1])}. Hai đoạn chồng nhau không sao vì min là luỹ đẳng.` });
      }
      return fr;
    },
    render(f) {
      const m = f.a.length;
      const data = f.st.map(row => Array.from({ length: m }, (_, i) => row[i] ?? ""));
      return table(data, {
        rowHead: f.st.map((_, j) => "2^" + j), colHead: f.a.map((_, i) => i),
        cls: (j, i) => f.q ? (j === f.q[2] && (i === f.q[0] || i === f.q[1] - (1 << f.q[2]) + 1) ? "on" : "") : (j === f.hj && data[j][i] !== "" ? "cur" : ""),
      }) + (f.q ? `<div class="muted small" style="margin-top:8px">Đoạn truy vấn</div>` + cells(f.a, i => i >= f.q[0] && i <= f.q[1] ? "hl" : "") : "");
    },
  };

  // 16. Segment tree -------------------------------------------------------------------
  DEFS.segtree = {
    title: "Cây phân đoạn (tổng)", params: [{ id: "a", label: "Dãy (≤ 8 số)", value: "5 8 6 3 2 7 2 6" }, { id: "q", label: "Truy vấn tổng l r", value: "2 6" }, { id: "u", label: "Cập nhật i v", value: "4 10" }],
    build(p) {
      let a = nums(p.a).slice(0, 8); while (a.length < 8) a.push(0); const t = Array(16).fill(0); const fr = [];
      const range = k => { let l = k, r = k; while (l < 8) { l = 2 * l; r = 2 * r + 1; } return [l - 8, r - 8]; };
      const snap = (cap, hl = [], on = []) => fr.push({ t: t.slice(), a: a.slice(), cap, hl, on, range: Array.from({ length: 16 }, (_, k) => k ? range(k) : null) });
      for (let i = 0; i < 8; i++) t[8 + i] = a[i];
      snap("Lá của cây là các phần tử của dãy.", [8, 9, 10, 11, 12, 13, 14, 15]);
      for (let k = 7; k >= 1; k--) { t[k] = t[2 * k] + t[2 * k + 1]; snap(`Nút ${k} quản lý đoạn [${range(k)}] = ${t[2 * k]} + ${t[2 * k + 1]} = ${t[k]}.`, [k], [2 * k, 2 * k + 1]); }
      const [l, r] = nums(p.q);
      if (l >= 0 && r < 8 && l <= r) {
        const used = [], seen = [];
        (function q(k, lo, hi) {
          seen.push(k);
          if (r < lo || hi < l) return;
          if (l <= lo && hi <= r) { used.push(k); return; }
          const m = (lo + hi) >> 1; q(2 * k, lo, m); q(2 * k + 1, m + 1, hi);
        })(1, 0, 7);
        snap(`Truy vấn tổng [${l}, ${r}]: chỉ cần ghép ${used.length} nút xanh (nằm trọn trong đoạn) = ${used.map(k => t[k]).join(" + ")} = ${used.reduce((s, k) => s + t[k], 0)}.`, seen.filter(k => !used.includes(k)), used);
      }
      const [ui, uv] = nums(p.u);
      if (ui >= 0 && ui < 8 && uv != null) {
        a[ui] = uv; let k = 8 + ui; t[k] = uv; const path = [k];
        while (k > 1) { k >>= 1; t[k] = t[2 * k] + t[2 * k + 1]; path.push(k); }
        snap(`Cập nhật a[${ui}] = ${uv}: chỉ các nút trên đường từ lá lên gốc thay đổi (${path.length} nút = O(log n)).`, path);
      }
      return fr;
    },
    render(f) {
      const ch = {}; for (let k = 1; k < 8; k++) ch[k] = [2 * k, 2 * k + 1];
      const pos = treePos(ch, 1, 640, 270);
      const nodes = []; for (let k = 1; k < 16; k++) nodes.push({ id: k, x: pos[k].x, y: pos[k].y, label: f.t[k], cls: f.on.includes(k) ? "on" : (f.hl.includes(k) ? "hl" : ""), sub: k >= 8 ? "a[" + (k - 8) + "]" : `[${f.range[k]}]` });
      const edges = []; for (let k = 2; k < 16; k++) edges.push({ u: k >> 1, v: k });
      return graph(nodes, edges, { w: 640, h: 300, r: 17 });
    },
  };

  // 17. Kruskal -----------------------------------------------------------------------
  DEFS.kruskal = {
    title: "Kruskal + DSU", params: [],
    build() {
      const order = G_W.map((e, k) => [e[2], e[0], e[1], k]).sort((x, y) => x[0] - y[0]);
      const par = {}; for (let i = 1; i <= 8; i++) par[i] = i;
      const find = x => par[x] === x ? x : (par[x] = find(par[x]));
      const take = [], skip = []; let tot = 0; const fr = [];
      const snap = (cap, cur) => fr.push({ take: take.slice(), skip: skip.slice(), cur, cap, par: { ...par }, tot });
      snap("Sắp xếp các cạnh theo trọng số tăng dần; mỗi đỉnh ban đầu là một tập riêng.", -1);
      for (const [w, u, v, k] of order) {
        const a = find(u), b = find(v);
        if (a !== b) { par[b] = a; take.push(k); tot += w; snap(`Cạnh ${u}–${v} (${w}) nối hai tập khác nhau ⇒ CHỌN. Tổng = ${tot}.`, k); }
        else { skip.push(k); snap(`Cạnh ${u}–${v} (${w}): ${u} và ${v} đã cùng tập ⇒ tạo chu trình, BỎ.`, k); }
      }
      snap(`Cây khung nhỏ nhất có tổng trọng số ${tot}.`, -1);
      return fr;
    },
    render(f) {
      const find = x => f.par[x] === x ? x : find(f.par[x]);
      const nodes = gNodes(id => ({ sub: "tập " + find(id) }));
      return graph(nodes, G_W.map(([u, v, w], k) => ({ u, v, label: w, cls: k === f.cur ? (f.take.includes(k) ? "hl" : "bad") : (f.take.includes(k) ? "on" : (f.skip.includes(k) ? "dim" : "")) }))) + kv({ "tổng": f.tot });
    },
  };

  // 18. Euler tour & LCA ----------------------------------------------------------------
  DEFS.euler = {
    title: "Euler tour, tin/tout và LCA", params: [{ id: "q", label: "LCA của u v", value: "8 6" }],
    build(p) {
      const ch = { 1: [2, 3], 2: [4, 5], 3: [6, 7], 5: [8, 9], 7: [10] };
      const tin = {}, tout = {}, dep = { 1: 0 }; let t = 0; const tour = []; const fr = [];
      const snap = (cap, cur) => fr.push({ ch, tin: { ...tin }, tout: { ...tout }, tour: tour.slice(), cap, cur });
      (function dfs(u) {
        tin[u] = t++; tour.push(u); snap(`Vào đỉnh ${u}: tin = ${tin[u]}. Euler tour ghi ${u}.`, u);
        for (const v of ch[u] || []) { dep[v] = dep[u] + 1; dfs(v); tour.push(u); snap(`Quay về ${u} từ ${v}: ghi ${u} vào Euler tour.`, u); }
        tout[u] = t - 1; snap(`Rời ${u}: tout = ${tout[u]}. Cây con của ${u} là đoạn [${tin[u]}, ${tout[u]}] theo tin.`, u);
      })(1);
      const [u, v] = nums(p.q);
      if (tin[u] != null && tin[v] != null) {
        const fu = tour.indexOf(u), fv = tour.indexOf(v); const [l, r] = [Math.min(fu, fv), Math.max(fu, fv)];
        let best = tour[l]; for (let i = l; i <= r; i++) if (dep[tour[i]] < dep[best]) best = tour[i];
        fr.push({ ch, tin: { ...tin }, tout: { ...tout }, tour: tour.slice(), cur: best, range: [l, r], lca: [u, v, best],
          cap: `LCA(${u}, ${v}): xét đoạn Euler tour giữa lần xuất hiện đầu của ${u} (vị trí ${fu}) và ${v} (vị trí ${fv}); đỉnh nông nhất là ${best}.` });
      }
      return fr;
    },
    render(f) {
      const pos = treePos(f.ch, 1, 620, 250);
      const nodes = Object.keys(pos).map(k => ({ id: +k, x: pos[k].x, y: pos[k].y, cls: f.lca && (f.lca[0] === +k || f.lca[1] === +k) ? "hl" : (+k === f.cur ? "cur" : (f.tin[k] != null ? "on" : "")), sub: f.tin[k] != null ? `${f.tin[k]}/${f.tout[k] ?? "?"}` : "" }));
      const edges = []; for (const u in f.ch) for (const v of f.ch[u]) edges.push({ u: +u, v });
      return graph(nodes, edges, { h: 280 }) + `<div class="muted small">Euler tour</div>` + cells(f.tour, i => f.range && i >= f.range[0] && i <= f.range[1] ? (f.tour[i] === f.lca[2] ? "on" : "hl") : "");
    },
  };

  // 19. Hash lăn (Rabin-Karp) -------------------------------------------------------------
  DEFS.hash = {
    title: "Hash lăn (Rabin–Karp)", params: [{ id: "t", label: "Văn bản", value: "abracadabra" }, { id: "p", label: "Mẫu", value: "abra" }],
    build(p) {
      const t = String(p.t).slice(0, 24), pt = String(p.p).slice(0, 8); const B = 31, M = 1000003, m = pt.length; const fr = [];
      const code = c => c.charCodeAt(0) - 96;
      let hp = 0; for (const c of pt) hp = (hp * B + code(c)) % M;
      let pw = 1; for (let i = 1; i < m; i++) pw = pw * B % M;
      fr.push({ t, m, i: -1, cap: `H("${pt}") = ${hp} với cơ số B = ${B}, modulo M = ${M}. Mỗi ký tự mã hoá a=1, b=2, ...`, hp, found: [] });
      let h = 0; const found = [];
      for (let i = 0; i < t.length; i++) {
        if (i >= m) h = ((h - code(t[i - m]) * pw) % M + M) % M;
        h = (h * B + code(t[i])) % M;
        if (i >= m - 1) {
          const st = i - m + 1; const match = h === hp && t.substr(st, m) === pt; if (match) found.push(st);
          fr.push({ t, m, i: st, h, hp, found: found.slice(), cap: `Cửa sổ "${t.substr(st, m)}" có hash ${h}${h === hp ? " = H(mẫu) ⇒ " + (match ? "khớp!" : "va chạm (kiểm tra lại thấy khác)") : " ≠ H(mẫu)"}. Trượt: bỏ ký tự đầu, thêm ký tự mới trong O(1).` });
        }
      }
      return fr;
    },
    render(f) {
      return cells(f.t.split(""), i => f.found.some(s => i >= s && i < s + f.m) ? "on" : (f.i >= 0 && i >= f.i && i < f.i + f.m ? "cur" : "")) + kv({ "hash mẫu": f.hp, "hash cửa sổ": f.h ?? "—", "vị trí khớp": f.found.join(", ") || "—" });
    },
  };

  // 20. Trie -----------------------------------------------------------------------------
  DEFS.trie = {
    title: "Trie: chèn từ", params: [{ id: "w", label: "Các từ", value: "an ant and bat bag ban" }],
    build(p) {
      const words = String(p.w).toLowerCase().split(/[\s,]+/).filter(Boolean).slice(0, 8);
      const nodes = [{ ch: {}, c: "∅", end: 0, cnt: 0 }]; const fr = [];
      const snap = (cap, path) => fr.push({ nodes: clone(nodes), path, cap });
      for (const w of words) {
        let u = 0; const path = [0]; nodes[0].cnt++;
        for (const c of w) {
          let created = false;
          if (nodes[u].ch[c] == null) { nodes[u].ch[c] = nodes.length; nodes.push({ ch: {}, c, end: 0, cnt: 0 }); created = true; }
          u = nodes[u].ch[c]; nodes[u].cnt++; path.push(u);
          snap(`Chèn "${w}": ký tự '${c}' — ${created ? "tạo nút mới" : "đi theo nút có sẵn (dùng chung tiền tố)"}.`, path.slice());
        }
        nodes[u].end++; snap(`Kết thúc "${w}": đánh dấu nút cuối (viền đỏ).`, path.slice());
      }
      snap(`Trie có ${nodes.length - 1} nút cho ${words.length} từ. Số dưới nút: số từ đi qua (cnt).`, []);
      return fr;
    },
    render(f) {
      const ch = {}; f.nodes.forEach((n, i) => { ch[i] = Object.values(n.ch); });
      const pos = treePos(ch, 0, 640, 300);
      const nodes = f.nodes.map((n, i) => ({ id: i, x: pos[i].x, y: pos[i].y, label: n.c, sub: n.cnt, cls: n.end ? "bad" : (f.path.includes(i) ? "cur" : "") }));
      const edges = []; f.nodes.forEach((n, i) => Object.values(n.ch).forEach(v => edges.push({ u: i, v, cls: f.path.includes(i) && f.path.includes(v) ? "hl" : "" })));
      return graph(nodes, edges, { w: 640, h: 330, r: 15 });
    },
  };

  // ------------------------------------------------------------ trình phát
  function mount(el, key) {
    const def = DEFS[key];
    if (!def) { el.innerHTML = `<div class="empty">Chưa có mô phỏng cho chuyên đề này.</div>`; return; }
    el.innerHTML = `<div class="viz"><div class="row"><h3 style="margin:0" class="grow">${esc(def.title)}</h3></div>
      <div class="viz-controls">${def.params.map(p => `<label class="small">${esc(p.label)} <input data-p="${p.id}" value="${esc(p.value)}" style="width:${String(p.value).length > 12 ? 260 : 90}px"></label>`).join("")}
        ${def.params.length ? `<button class="btn" data-a="rebuild">Áp dụng</button>` : ""}</div>
      <div class="viz-controls"><button class="btn" data-a="first">⏮</button><button class="btn" data-a="prev">◀</button>
        <button class="btn primary" data-a="play">▶ Chạy</button><button class="btn" data-a="next">▶|</button><button class="btn" data-a="last">⏭</button>
        <label class="small">Tốc độ <input type="range" min="1" max="10" value="5" data-a="speed"></label><span class="small muted" data-a="pos"></span></div>
      <div class="viz-stage"></div><div class="viz-caption"></div></div>`;
    const stage = el.querySelector(".viz-stage"), cap = el.querySelector(".viz-caption"), posEl = el.querySelector('[data-a="pos"]');
    const playBtn = el.querySelector('[data-a="play"]'), speed = el.querySelector('[data-a="speed"]');
    let frames = [], i = 0, timer = null;
    const params = () => { const o = {}; el.querySelectorAll("[data-p]").forEach(x => o[x.dataset.p] = x.value); return o; };
    const draw = () => {
      if (!frames.length) { stage.innerHTML = '<div class="empty">Không có dữ liệu.</div>'; return; }
      const f = frames[i]; stage.innerHTML = def.render(f); cap.textContent = f.cap || ""; posEl.textContent = `Bước ${i + 1}/${frames.length}`;
    };
    const stop = () => { clearInterval(timer); timer = null; playBtn.textContent = "▶ Chạy"; };
    const play = () => {
      if (timer) return stop();
      if (i >= frames.length - 1) i = 0;
      playBtn.textContent = "⏸ Dừng";
      const tick = () => { if (!document.body.contains(el)) return stop(); if (i < frames.length - 1) { i++; draw(); } else stop(); };
      timer = setInterval(tick, 1100 - speed.value * 100);
    };
    const rebuild = () => { stop(); try { frames = def.build(params()); } catch (e) { frames = []; } i = 0; draw(); };
    el.addEventListener("click", e => {
      const a = e.target.closest("[data-a]")?.dataset.a; if (!a) return;
      if (a === "rebuild") rebuild();
      if (a === "play") play();
      if (a === "first") { stop(); i = 0; draw(); }
      if (a === "last") { stop(); i = frames.length - 1; draw(); }
      if (a === "prev") { stop(); i = Math.max(0, i - 1); draw(); }
      if (a === "next") { stop(); i = Math.min(frames.length - 1, i + 1); draw(); }
    });
    speed.addEventListener("input", () => { if (timer) { stop(); play(); } });
    el.querySelectorAll("[data-p]").forEach(x => x.addEventListener("keydown", e => { if (e.key === "Enter") rebuild(); }));
    rebuild();
  }

  window.VIZ = { mount, DEFS };
})();
