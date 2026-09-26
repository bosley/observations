const $ = (id) => document.getElementById(id);

let graph = null;
const sectionById = {};
let lastRead = "";
let cy = null;
let chapterCounts = null;

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function snippet(text, n) {
  const t = String(text).replace(/\s+/g, " ").trim();
  const max = n || 88;
  return t.length > max ? t.slice(0, max - 1) + "…" : t;
}

function numLink(id) {
  const ok = graph.propositions[id];
  const cls = ok ? "" : ' class="missing"';
  return `<a href="#${id}"${cls}>${id}</a>`;
}

function renderInline(text) {
  const escaped = escapeHtml(text);
  const re = /`([^`]+)`|(\d+\.\d+)([–-])(\d+\.\d+)|(\d+\.\d+)/g;
  let html = "";
  let last = 0;
  let m;
  while ((m = re.exec(escaped))) {
    html += escaped.slice(last, m.index);
    if (m[1] !== undefined) html += `<code>${m[1]}</code>`;
    else if (m[2] !== undefined) html += numLink(m[2]) + m[3] + numLink(m[4]);
    else html += numLink(m[5]);
    last = m.index + m[0].length;
  }
  return html + escaped.slice(last);
}

function parseSel(hash) {
  const h = decodeURIComponent((hash || "").replace(/^#/, ""));
  if (!h) {
    const first = graph.sections[0];
    return { kind: first.kind, id: first.id };
  }
  if (h.startsWith("glossary/")) {
    const tid = h.slice(9);
    if (graph.terms[tid]) return { kind: "glossary", id: "glossary", term: tid };
    return { kind: "glossary", id: "glossary" };
  }
  if (graph.propositions[h]) {
    const p = graph.propositions[h];
    return { kind: "chapter", id: p.chapter, prop: h };
  }
  const s = sectionById[h];
  if (s) return { kind: s.kind, id: s.id };
  return { kind: graph.sections[0].kind, id: graph.sections[0].id };
}

function selKey(sel) {
  if (sel.kind === "glossary") return "glossary:" + (sel.term || "");
  if (sel.prop) return "prop:" + sel.prop;
  return sel.kind + ":" + sel.id;
}

function readKey(sel) {
  return sel.kind + ":" + sel.id;
}

function navHref(s) {
  return "#" + s.id;
}

function renderNav(sel, q) {
  const box = $("nav-list");
  const query = (q || "").trim().toLowerCase();
  if (!query) {
    box.innerHTML = graph.sections
      .map((s) => {
        const on = s.id === sel.id && !sel.prop && !sel.term ? " on" : "";
        const num =
          s.kind === "chapter" ? `<span class="num">${s.number}</span> ` : "";
        return `<a class="${on.trim()}" href="${navHref(s)}">${num}${escapeHtml(s.title)}</a>`;
      })
      .join("");
    return;
  }
  const hits = [];
  const numQ = /^\d+(\.\d*)?$/.test(query);
  for (const s of graph.sections) {
    const hay = ((s.number ? s.number + " " : "") + s.title).toLowerCase();
    if (numQ) {
      if (String(s.number) === query) hits.push({ kind: "section", s });
    } else if (hay.includes(query) || s.id.toLowerCase().includes(query)) {
      hits.push({ kind: "section", s });
    }
  }
  for (const pid of graph.order) {
    const p = graph.propositions[pid];
    const idHit = query.includes(".")
      ? pid === query || pid.startsWith(query)
      : pid === query || pid.startsWith(query + ".");
    if (numQ ? idHit : (pid.toLowerCase().includes(query) || p.text.toLowerCase().includes(query))) {
      hits.push({ kind: "prop", p });
    }
  }
  for (const t of Object.values(graph.terms)) {
    if (numQ) {
      if (t.cites.some((c) => c === query || c.startsWith(query + "."))) {
        hits.push({ kind: "term", t });
      }
    } else if (
      t.term.toLowerCase().includes(query) ||
      t.id.includes(query) ||
      t.text.toLowerCase().includes(query)
    ) {
      hits.push({ kind: "term", t });
    }
  }
  if (!hits.length) {
    box.innerHTML = `<p class="hit">No matches</p>`;
    return;
  }
  const parts = [];
  let lastKind = "";
  const labels = { section: "Sections", prop: "Propositions", term: "Terms" };
  for (const hit of hits) {
    if (hit.kind !== lastKind) {
      parts.push(`<p class="hit">${labels[hit.kind]}</p>`);
      lastKind = hit.kind;
    }
    if (hit.kind === "section") {
      const on = hit.s.id === sel.id && !sel.prop && !sel.term ? " on" : "";
      const num =
        hit.s.kind === "chapter" ? `<span class="num">${hit.s.number}</span> ` : "";
      parts.push(
        `<a class="${on.trim()}" href="${navHref(hit.s)}">${num}${escapeHtml(hit.s.title)}</a>`
      );
    } else if (hit.kind === "prop") {
      const on = sel.prop === hit.p.id ? " on" : "";
      parts.push(
        `<a class="sub${on}" href="#${hit.p.id}"><span class="num">${hit.p.id}</span> ${escapeHtml(snippet(hit.p.text, 52))}</a>`
      );
    } else {
      const on = sel.term === hit.t.id ? " on" : "";
      parts.push(
        `<a class="sub${on}" href="#glossary/${hit.t.id}">${escapeHtml(hit.t.term)}</a>`
      );
    }
  }
  box.innerHTML = parts.join("");
}

function renderCenter(sel) {
  const el = $("read");
  const key = readKey(sel);
  if (key !== lastRead) {
    lastRead = key;
    const s = sectionById[sel.id];
    if (s.kind === "prose") {
      el.innerHTML =
        `<h1>${escapeHtml(s.title)}</h1>` +
        s.blocks
          .map((b) => `<p>${renderInline(b.text)}</p>`)
          .join("");
      el.scrollTop = 0;
    } else if (s.kind === "chapter") {
      let html = `<h1><span class="num">${s.number}.</span> ${escapeHtml(s.title)}</h1>`;
      for (const b of s.blocks) {
        if (b.type === "heading") html += `<h2>${escapeHtml(b.text)}</h2>`;
        else if (b.type === "prose") html += `<p>${renderInline(b.text)}</p>`;
        else if (b.type === "proposition") {
          const p = graph.propositions[b.id];
          html += `<article class="prop" data-id="${b.id}"><h3><a href="#${b.id}">${b.id}</a></h3><p>${renderInline(p.text)}</p></article>`;
        }
      }
      el.innerHTML = html;
    } else if (s.kind === "glossary") {
      let html = `<h1>${escapeHtml(s.title)}</h1>`;
      for (const b of s.blocks) {
        if (b.type === "prose") html += `<p>${renderInline(b.text)}</p>`;
      }
      for (const tid of s.termIds) {
        const t = graph.terms[tid];
        html += `<article class="term" data-id="${tid}"><h3><a href="#glossary/${tid}">${escapeHtml(t.term)}</a></h3><p>${renderInline(t.text)}</p></article>`;
      }
      el.innerHTML = html;
    }
  }
  el.querySelectorAll(".prop.on, .term.on").forEach((n) => n.classList.remove("on"));
  let target = null;
  if (sel.prop) target = el.querySelector(`.prop[data-id="${CSS.escape(sel.prop)}"]`);
  if (sel.term) target = el.querySelector(`.term[data-id="${CSS.escape(sel.term)}"]`);
  if (target) {
    target.classList.add("on");
    target.scrollIntoView({ block: "start", inline: "nearest", behavior: "auto" });
  } else if (!sel.prop && !sel.term) {
    el.scrollTop = 0;
  }
}

function propItem(id) {
  const p = graph.propositions[id];
  if (!p) return `<li class="missing">${escapeHtml(id)}</li>`;
  return `<li><a href="#${id}"><span class="num">${id}</span> <span class="snip">${escapeHtml(snippet(p.text, 70))}</span></a></li>`;
}

function listBlock(title, ids, empty) {
  if (!ids || !ids.length) return `<h3>${title}</h3><p class="empty">${empty || "None"}</p>`;
  return `<h3>${title}</h3><ul>${ids.map(propItem).join("")}</ul>`;
}

function chapterTitle(id) {
  const s = sectionById[id];
  return s ? `${s.number}. ${s.title}` : id;
}

function chapterLinkCounts(sid) {
  const out = {};
  const inn = {};
  for (const pid of graph.order) {
    const p = graph.propositions[pid];
    for (const c of p.cites) {
      const t = graph.propositions[c];
      if (!t) continue;
      if (p.chapter === sid && t.chapter !== sid) {
        out[t.chapter] = (out[t.chapter] || 0) + 1;
      }
      if (t.chapter === sid && p.chapter !== sid) {
        inn[p.chapter] = (inn[p.chapter] || 0) + 1;
      }
    }
  }
  const rows = (map) =>
    Object.keys(map)
      .sort((a, b) => Number(a) - Number(b))
      .map((id) => {
        return `<li><a href="#${id}"><span class="num">${escapeHtml(chapterTitle(id))}</span> <span class="snip">${map[id]}</span></a></li>`;
      })
      .join("");
  return { outHtml: rows(out), innHtml: rows(inn), out, inn };
}

function renderPanel(sel) {
  const el = $("panel");
  if (sel.prop) {
    const p = graph.propositions[sel.prop];
    const terms = p.terms
      .map((tid) => {
        const t = graph.terms[tid];
        return `<li><a href="#glossary/${tid}">${escapeHtml(t.term)}</a></li>`;
      })
      .join("");
    el.innerHTML =
      `<h2>${p.id}</h2>` +
      (p.parent
        ? `<h3>Parent</h3><ul>${propItem(p.parent)}</ul>`
        : `<h3>Parent</h3><p class="empty">Chapter ${p.chapter}</p>`) +
      listBlock("Children", p.children) +
      listBlock("Cites", p.cites) +
      listBlock("Cited by", p.citedBy) +
      (p.unresolved.length
        ? `<h3>Missing</h3><ul>${p.unresolved.map((u) => `<li class="missing">${escapeHtml(u)}</li>`).join("")}</ul>`
        : "") +
      (p.terms.length ? `<h3>Glossary</h3><ul>${terms}</ul>` : "");
    drawNeighborhood(p);
    return;
  }
  if (sel.term) {
    const t = graph.terms[sel.term];
    el.innerHTML =
      `<h2>${escapeHtml(t.term)}</h2>` +
      listBlock("Cites", t.cites) +
      (t.unresolved.length
        ? `<h3>Missing</h3><ul>${t.unresolved.map((u) => `<li class="missing">${escapeHtml(u)}</li>`).join("")}</ul>`
        : "");
    drawHub(t.term, t.cites);
    return;
  }
  const s = sectionById[sel.id];
  if (s.kind === "chapter") {
    const links = chapterLinkCounts(s.id);
    el.innerHTML =
      `<h2>${s.number}. ${escapeHtml(s.title)}</h2>` +
      `<p class="empty">${s.propositionIds.length} propositions</p>` +
      `<h3>Cites</h3>${links.outHtml ? `<ul>${links.outHtml}</ul>` : `<p class="empty">None</p>`}` +
      `<h3>Cited by</h3>${links.innHtml ? `<ul>${links.innHtml}</ul>` : `<p class="empty">None</p>`}` +
      (s.unresolved.length
        ? `<h3>Missing</h3><ul>${s.unresolved.map((u) => `<li class="missing">${escapeHtml(u)}</li>`).join("")}</ul>`
        : "");
    drawChapters(s.id);
    return;
  }
  el.innerHTML =
    `<h2>${escapeHtml(s.title)}</h2>` +
    listBlock("Cites", s.cites) +
    (s.unresolved.length
      ? `<h3>Missing</h3><ul>${s.unresolved.map((u) => `<li class="missing">${escapeHtml(u)}</li>`).join("")}</ul>`
      : "");
  if (s.cites && s.cites.length) drawHub(s.title, s.cites);
  else clearGraph();
}

function clearGraph() {
  if (cy) {
    cy.destroy();
    cy = null;
  }
  $("graph").hidden = true;
}

function hasCy() {
  return typeof cytoscape === "function";
}

function startCy(elements, layout, focusId) {
  if (!hasCy() || !elements.length) {
    clearGraph();
    return;
  }
  const box = $("graph");
  box.hidden = false;
  if (cy) {
    cy.destroy();
    cy = null;
  }
  cy = cytoscape({
    container: box,
    elements,
    layout,
    userZoomingEnabled: true,
    userPanningEnabled: true,
    boxSelectionEnabled: false,
    style: [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "font-size": 9,
          "font-family": "system-ui, sans-serif",
          color: "#1b1714",
          "background-color": "#cfc4ae",
          "border-width": 1,
          "border-color": "#6a6359",
          width: 22,
          height: 22,
          "text-valign": "bottom",
          "text-margin-y": 4,
        },
      },
      {
        selector: "node[kind = 'focus']",
        style: {
          "background-color": "#6a3224",
          "border-color": "#3d1c14",
          color: "#1b1714",
          width: 28,
          height: 28,
          "font-weight": 600,
        },
      },
      {
        selector: "edge",
        style: {
          width: "data(weight)",
          "line-color": "#8a6a50",
          "target-arrow-color": "#8a6a50",
          "target-arrow-shape": "triangle",
          "arrow-scale": 0.7,
          "curve-style": "bezier",
        },
      },
      {
        selector: "edge[kind = 'parent']",
        style: {
          "line-style": "dashed",
          "line-color": "#6a6359",
          "target-arrow-color": "#6a6359",
          width: 1.2,
        },
      },
    ],
  });
  cy.on("tap", "node", (evt) => {
    const href = evt.target.data("href");
    if (href) location.hash = href;
  });
  if (focusId) {
    const n = cy.getElementById(focusId);
    if (n && n.length) cy.center(n);
  }
}

function addNode(nodes, seen, id, label, kind, href) {
  if (seen.has(id)) return;
  seen.add(id);
  nodes.push({ data: { id, label, kind: kind || "node", href } });
}

function drawNeighborhood(p) {
  const nodes = [];
  const edges = [];
  const seen = new Set();
  addNode(nodes, seen, p.id, p.id, "focus", p.id);
  for (const c of p.cites) {
    addNode(nodes, seen, c, c, "node", c);
    edges.push({ data: { id: p.id + ">" + c, source: p.id, target: c, kind: "cite", weight: 1.4 } });
  }
  for (const c of p.citedBy) {
    addNode(nodes, seen, c, c, "node", c);
    edges.push({ data: { id: c + ">" + p.id, source: c, target: p.id, kind: "cite", weight: 1.4 } });
  }
  if (p.parent) {
    addNode(nodes, seen, p.parent, p.parent, "node", p.parent);
    edges.push({
      data: { id: "p:" + p.parent + ">" + p.id, source: p.parent, target: p.id, kind: "parent", weight: 1.2 },
    });
  }
  for (const c of p.children) {
    addNode(nodes, seen, c, c, "node", c);
    edges.push({
      data: { id: "p:" + p.id + ">" + c, source: p.id, target: c, kind: "parent", weight: 1.2 },
    });
  }
  startCy(
    nodes.concat(edges),
    {
      name: "cose",
      animate: false,
      padding: 18,
      nodeRepulsion: function () { return 9000; },
      idealEdgeLength: function () { return 70; },
      gravity: 0.3,
    },
    p.id
  );
}

function drawHub(label, ids) {
  const nodes = [];
  const edges = [];
  const seen = new Set();
  const hub = "__hub__";
  addNode(nodes, seen, hub, label, "focus", null);
  for (const id of ids) {
    addNode(nodes, seen, id, id, "node", id);
    edges.push({ data: { id: hub + ">" + id, source: hub, target: id, kind: "cite", weight: 1.3 } });
  }
  const hold = new Set(ids);
  for (const id of ids) {
    const p = graph.propositions[id];
    if (!p) continue;
    for (const c of p.cites) {
      if (!hold.has(c)) continue;
      edges.push({ data: { id: id + ">" + c, source: id, target: c, kind: "cite", weight: 1 } });
    }
  }
  startCy(nodes.concat(edges), { name: "cose", animate: false, padding: 16 }, hub);
}

function buildChapterCounts() {
  const counts = {};
  for (const pid of graph.order) {
    const p = graph.propositions[pid];
    for (const c of p.cites) {
      const t = graph.propositions[c];
      if (!t || t.chapter === p.chapter) continue;
      const k = p.chapter + ">" + t.chapter;
      counts[k] = (counts[k] || 0) + 1;
    }
  }
  return counts;
}

function drawChapters(focus) {
  if (!chapterCounts) chapterCounts = buildChapterCounts();
  const chapters = graph.sections.filter((s) => s.kind === "chapter");
  const nodes = chapters.map((s) => ({
    data: {
      id: s.id,
      label: String(s.number),
      kind: s.id === focus ? "focus" : "node",
      href: s.id,
    },
  }));
  const edges = Object.keys(chapterCounts).map((k) => {
    const [source, target] = k.split(">");
    const n = chapterCounts[k];
    return {
      data: {
        id: k,
        source,
        target,
        kind: "cite",
        weight: Math.min(7, 1 + Math.log2(n + 1)),
      },
    };
  });
  startCy(
    nodes.concat(edges),
    { name: "circle", animate: false, padding: 22, sweep: Math.PI * 2, clockwise: true },
    focus
  );
}

function apply() {
  const sel = parseSel(location.hash);
  document.title = sectionById[sel.id]
    ? sectionById[sel.id].title + " — " + (graph.meta.title || "Tractate")
    : graph.meta.title || "Tractate";
  renderNav(sel, $("search").value);
  renderCenter(sel);
  renderPanel(sel);
}

async function boot() {
  const res = await fetch("/api/graph");
  graph = await res.json();
  for (const s of graph.sections) sectionById[s.id] = s;
  $("doc-title").textContent = graph.meta.title || "Tractate";
  const bits = [graph.meta.author, graph.meta.date].filter(Boolean);
  $("doc-byline").textContent = bits.join(", ");
  $("status").textContent =
    graph.order.length + " propositions · " + Object.keys(graph.terms).length + " terms";
  $("search").addEventListener("input", () => {
    renderNav(parseSel(location.hash), $("search").value);
  });
  window.addEventListener("hashchange", apply);
  apply();
}

boot().catch((err) => {
  $("status").textContent = "failed to load";
  $("read").innerHTML = `<h1>Could not load</h1><p>${escapeHtml(err.message)}</p>`;
});
