import re
from pathlib import Path

OPENXML_RE = re.compile(r"```\{=openxml\}.*?```", re.DOTALL)
PROP_LINE_RE = re.compile(r"^\*\*(\d+\.\d+)\*\*\s*(.*)$")
CHAPTER_RE = re.compile(r"^## (\d+)\.\s+(.+)$")
HEADING_RE = re.compile(r"^## (.+)$")
SUBHEAD_RE = re.compile(r"^### (.+)$")
TERM_RE = re.compile(r"^\*\*(.+)\*\*\s*$")
DEF_RE = re.compile(r"^:\s+(.*)$")
RANGE_RE = re.compile(r"(\d+\.\d+)[–-](\d+\.\d+)")
SINGLE_RE = re.compile(r"(?<![\d.])(\d+\.\d+)(?![\d.])")


def slug(term):
    s = term.strip().strip('"').lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def split_frontmatter(raw):
    meta = {}
    if not raw.startswith("---"):
        return meta, raw
    end = raw.find("\n---", 3)
    if end < 0:
        return meta, raw
    block = raw[3:end]
    body = raw[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip().strip('"')
    return meta, body


def numbering_parent(pid, known):
    if "." not in pid:
        return None
    chap, frac = pid.split(".", 1)
    if len(frac) <= 1:
        return None
    while len(frac) > 1:
        frac = frac[:-1]
        cand = f"{chap}.{frac}"
        if cand in known:
            return cand
    return None


def extract_cites(text, known, order, order_index, self_id=None):
    cites = []
    unresolved = []
    seen = set()
    range_spans = []

    def add(pid):
        if self_id and pid == self_id:
            return
        if pid in seen:
            return
        seen.add(pid)
        if pid in known:
            cites.append(pid)
        else:
            unresolved.append(pid)

    for m in RANGE_RE.finditer(text):
        range_spans.append(m.span())
        a, b = m.group(1), m.group(2)
        if a in order_index and b in order_index:
            i, j = order_index[a], order_index[b]
            if i > j:
                i, j = j, i
            for pid in order[i : j + 1]:
                add(pid)
        else:
            add(a)
            add(b)

    for m in SINGLE_RE.finditer(text):
        span = m.span()
        if any(span[0] >= s[0] and span[1] <= s[1] for s in range_spans):
            continue
        add(m.group(1))

    return cites, unresolved


def flush_paras(buf, blocks):
    text = "\n".join(buf).strip()
    buf.clear()
    if text:
        blocks.append({"type": "prose", "text": text})


def parse(path):
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(raw)
    body = OPENXML_RE.sub("\n", body)
    lines = body.splitlines()

    sections = []
    propositions = {}
    terms = {}
    order = []

    i = 0
    n = len(lines)

    def skip_blank():
        nonlocal i
        while i < n and not lines[i].strip():
            i += 1

    while i < n:
        line = lines[i]
        if not line.startswith("## "):
            i += 1
            continue

        chapter_m = CHAPTER_RE.match(line)
        heading_m = HEADING_RE.match(line)
        title = heading_m.group(1).strip() if heading_m else ""
        i += 1

        if title == "Contents":
            while i < n and not lines[i].startswith("## "):
                i += 1
            continue

        if chapter_m:
            number = int(chapter_m.group(1))
            chap_title = chapter_m.group(2).strip()
            sid = str(number)
            blocks = []
            prop_ids = []
            buf = []
            current = None

            def close_prop():
                nonlocal current
                if current is None:
                    return
                current["text"] = current["text"].strip()
                propositions[current["id"]] = current
                order.append(current["id"])
                prop_ids.append(current["id"])
                blocks.append({"type": "proposition", "id": current["id"]})
                current = None

            while i < n and not lines[i].startswith("## "):
                row = lines[i]
                sub = SUBHEAD_RE.match(row)
                prop = PROP_LINE_RE.match(row)
                if sub:
                    close_prop()
                    flush_paras(buf, blocks)
                    blocks.append({"type": "heading", "text": sub.group(1).strip()})
                    i += 1
                    continue
                if prop:
                    close_prop()
                    flush_paras(buf, blocks)
                    current = {
                        "id": prop.group(1),
                        "chapter": sid,
                        "text": prop.group(2),
                        "parent": None,
                        "children": [],
                        "cites": [],
                        "citedBy": [],
                        "unresolved": [],
                        "terms": [],
                    }
                    i += 1
                    continue
                if current is not None:
                    if row.strip():
                        if current["text"]:
                            current["text"] += "\n" + row
                        else:
                            current["text"] = row
                    else:
                        close_prop()
                    i += 1
                    continue
                if row.strip():
                    buf.append(row)
                else:
                    flush_paras(buf, blocks)
                i += 1

            close_prop()
            flush_paras(buf, blocks)
            sections.append(
                {
                    "id": sid,
                    "kind": "chapter",
                    "number": number,
                    "title": chap_title,
                    "propositionIds": prop_ids,
                    "blocks": blocks,
                    "cites": [],
                    "unresolved": [],
                }
            )
            continue

        if title == "Glossary":
            blocks = []
            term_ids = []
            buf = []
            pending_term = None
            while i < n and not lines[i].startswith("## "):
                row = lines[i]
                term_m = TERM_RE.match(row)
                def_m = DEF_RE.match(row)
                if pending_term is not None and def_m:
                    flush_paras(buf, blocks)
                    tid = slug(pending_term)
                    text = def_m.group(1).strip()
                    i += 1
                    while i < n and not lines[i].startswith("## "):
                        cont = lines[i]
                        if TERM_RE.match(cont) or DEF_RE.match(cont) or not cont.strip():
                            break
                        text += " " + cont.strip()
                        i += 1
                    terms[tid] = {
                        "id": tid,
                        "term": pending_term,
                        "text": text,
                        "cites": [],
                        "unresolved": [],
                    }
                    term_ids.append(tid)
                    pending_term = None
                    continue
                if term_m and not PROP_LINE_RE.match(row):
                    flush_paras(buf, blocks)
                    pending_term = term_m.group(1)
                    i += 1
                    continue
                if row.strip():
                    buf.append(row)
                else:
                    flush_paras(buf, blocks)
                i += 1
            flush_paras(buf, blocks)
            sections.append(
                {
                    "id": "glossary",
                    "kind": "glossary",
                    "title": "Glossary",
                    "termIds": term_ids,
                    "blocks": blocks,
                    "cites": [],
                    "unresolved": [],
                }
            )
            continue

        sid = slug(title)
        blocks = []
        buf = []
        while i < n and not lines[i].startswith("## "):
            row = lines[i]
            if row.strip():
                buf.append(row)
            else:
                flush_paras(buf, blocks)
            i += 1
        flush_paras(buf, blocks)
        sections.append(
            {
                "id": sid,
                "kind": "prose",
                "title": title,
                "blocks": blocks,
                "cites": [],
                "unresolved": [],
            }
        )

    known = set(order)
    order_index = {pid: idx for idx, pid in enumerate(order)}

    for pid, prop in propositions.items():
        parent = numbering_parent(pid, known)
        prop["parent"] = parent
        if parent:
            propositions[parent]["children"].append(pid)

    for pid in order:
        children = propositions[pid]["children"]
        children.sort(key=lambda c: order_index[c])

    for pid, prop in propositions.items():
        cites, unresolved = extract_cites(
            prop["text"], known, order, order_index, self_id=pid
        )
        prop["cites"] = cites
        prop["unresolved"] = unresolved

    for pid, prop in propositions.items():
        for c in prop["cites"]:
            propositions[c]["citedBy"].append(pid)

    for pid in order:
        cited = propositions[pid]["citedBy"]
        cited.sort(key=lambda c: order_index[c])

    for term in terms.values():
        cites, unresolved = extract_cites(
            term["text"], known, order, order_index
        )
        term["cites"] = cites
        term["unresolved"] = unresolved
        for c in cites:
            propositions[c]["terms"].append(term["id"])

    for pid in order:
        propositions[pid]["terms"].sort()

    for section in sections:
        if section["kind"] == "prose":
            blob = "\n".join(
                b["text"] for b in section["blocks"] if b["type"] == "prose"
            )
            cites, unresolved = extract_cites(blob, known, order, order_index)
            section["cites"] = cites
            section["unresolved"] = unresolved
        elif section["kind"] == "chapter":
            seen = []
            hold = set()
            unresolved = []
            uhold = set()
            for pid in section["propositionIds"]:
                for c in propositions[pid]["cites"]:
                    if c not in hold:
                        hold.add(c)
                        seen.append(c)
                for u in propositions[pid]["unresolved"]:
                    if u not in uhold:
                        uhold.add(u)
                        unresolved.append(u)
            section["cites"] = seen
            section["unresolved"] = unresolved

    return {
        "meta": {
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "date": meta.get("date", ""),
        },
        "order": order,
        "sections": sections,
        "propositions": propositions,
        "terms": terms,
    }
