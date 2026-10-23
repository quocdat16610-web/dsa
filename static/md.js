// Trình hiển thị Markdown tối giản (tiêu đề, đoạn, danh sách, bảng, khối code, trích dẫn, in đậm/nghiêng, code nội dòng).
(function () {
  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function inline(s) {
    const codes = [];
    s = s.replace(/`([^`]+)`/g, (_, c) => { codes.push(c); return "\u0000" + (codes.length - 1) + "\u0000"; });
    s = esc(s);
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
         .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>")
         .replace(/(^|\W)_([^_]+)_(?=\W|$)/g, "$1<em>$2</em>")
         .replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
         .replace(/(\d+)\^(\d+|\(?[a-z0-9+\-−]+\)?)/gi, (m, a, b) => a + "<sup>" + b.replace(/^\((.*)\)$/, "$1") + "</sup>");
    s = s.replace(/\u0000(\d+)\u0000/g, (_, i) => "<code>" + supInCode(esc(codes[+i])) + "</code>");
    return s;
  }
  function supInCode(s) {
    return s.replace(/(\d+)\^(\d+)/g, "$1<sup>$2</sup>");
  }
  function highlight(code, lang) {
    let s = esc(code);
    if (!/cpp|c\+\+|py|^$/.test(lang || "")) return s;
    const kw = /\b(int|long|double|bool|char|void|return|for|while|if|else|const|auto|vector|string|struct|using|namespace|include|true|false|break|continue|def|in|range|and|or|not|class|stack|queue|deque|map|set|pair|priority_queue|multiset|unsigned|static|swap|min|max)\b/g;
    const parts = s.split(/(\/\/[^\n]*|#[^\n]*)/g);
    return parts.map((p, i) => {
      if (i % 2 === 1) return '<span class="c-com">' + p + "</span>";
      return p.replace(kw, '<span class="c-kw">$1</span>').replace(/\b(\d+)\b/g, '<span class="c-num">$1</span>');
    }).join("");
  }
  function render(md) {
    const lines = md.replace(/\r/g, "").split("\n");
    let out = [], i = 0;
    while (i < lines.length) {
      let ln = lines[i];
      if (/^```/.test(ln)) {
        const lang = ln.slice(3).trim(); const buf = []; i++;
        while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]);
        i++;
        out.push('<pre class="code"><button class="copy" type="button">Sao chép</button><code>' + highlight(buf.join("\n"), lang) + "</code></pre>");
        continue;
      }
      let m = ln.match(/^(#{1,4})\s+(.*)$/);
      if (m) { const h = m[1].length + 1; out.push(`<h${h}>${inline(m[2])}</h${h}>`); i++; continue; }
      if (/^\|/.test(ln)) {
        const rows = [];
        while (i < lines.length && /^\|/.test(lines[i])) rows.push(lines[i++]);
        const cells = r => r.replace(/^\||\|$/g, "").split(/(?<!\\)\|/).map(c => inline(c.trim().replace(/\\\|/g, "|")));
        let html = "<table class='md-table'><thead><tr>" + cells(rows[0]).map(c => `<th>${c}</th>`).join("") + "</tr></thead><tbody>";
        rows.slice(2).forEach(r => { html += "<tr>" + cells(r).map(c => `<td>${c}</td>`).join("") + "</tr>"; });
        out.push(html + "</tbody></table>");
        continue;
      }
      if (/^\s*[-*]\s+/.test(ln) || /^\s*\d+\.\s+/.test(ln)) {
        const ordered = /^\s*\d+\./.test(ln); const items = [];
        while (i < lines.length && (/^\s*[-*]\s+/.test(lines[i]) || /^\s*\d+\.\s+/.test(lines[i]) || (/^\s{2,}\S/.test(lines[i]) && items.length))) {
          const l = lines[i++];
          if (/^\s{2,}\S/.test(l) && !/^\s*([-*]|\d+\.)\s+/.test(l)) items[items.length - 1] += " " + l.trim();
          else items.push(l.replace(/^\s*([-*]|\d+\.)\s+/, ""));
        }
        const tag = ordered ? "ol" : "ul";
        out.push(`<${tag}>` + items.map(it => `<li>${inline(it)}</li>`).join("") + `</${tag}>`);
        continue;
      }
      if (/^>\s?/.test(ln)) {
        const buf = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) buf.push(lines[i++].replace(/^>\s?/, ""));
        out.push("<blockquote>" + inline(buf.join(" ")) + "</blockquote>");
        continue;
      }
      if (!ln.trim()) { i++; continue; }
      const buf = [];
      while (i < lines.length && lines[i].trim() && !/^(#|```|\||>|\s*[-*]\s|\s*\d+\.\s)/.test(lines[i])) buf.push(lines[i++]);
      out.push("<p>" + inline(buf.join(" ")) + "</p>");
    }
    return out.join("\n");
  }
  window.MD = { render, inline, esc };
})();
