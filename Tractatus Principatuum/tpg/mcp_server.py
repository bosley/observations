import re

from parse import slug

PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"]
SERVER_VERSION = "1.0.0"
RANGE_ID_RE = re.compile(r"^(\d+\.\d+)\s*[–-]\s*(\d+\.\d+)$")
NUM_RE = re.compile(r"^\d+(\.\d*)?$")
STATED_COUNT_RE = re.compile(r"\b\d+\b(?=\s+(?:short\s+)?numbered propositions\b)")
MAX_IDS = 120
SOURCE_URL = "https://github.com/bosley/observations"


class RpcError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def clip(text, n=160):
    t = " ".join(str(text).split())
    return t if len(t) <= n else t[: n - 1] + "…"


def around(text, needle, n=180):
    t = " ".join(str(text).split())
    i = t.lower().find(needle)
    if i < 0 or len(t) <= n:
        return clip(t, n)
    start = max(0, i - n // 3)
    end = start + n
    return ("…" if start else "") + t[start:end] + ("…" if end < len(t) else "")


TOOLS = [
    {
        "name": "get_overview",
        "title": "Overview",
        "description": "Title, author, size, how proposition numbering and citations work, and the list of section ids. Call this first.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "read_full",
        "title": "Read the full tractate",
        "description": "Return the entire tractate as Markdown: preface, every chapter with all numbered propositions, and the glossary. Roughly 25k tokens.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "read_section",
        "title": "Read a section",
        "description": "Return one section as Markdown. Accepts a chapter number (e.g. \"3\"), a section id from get_overview (e.g. \"preface\", \"glossary\"), or a section title.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "Chapter number, section id, or title"}
            },
            "required": ["section"],
        },
    },
    {
        "name": "get_propositions",
        "title": "Get propositions",
        "description": "Return numbered propositions by id, with their parent, children, what they cite, what cites them, and linked glossary terms. Ids look like \"3.02\"; ranges like \"3.0-3.3\" are expanded in document order.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Proposition ids or ranges",
                },
                "include_related": {
                    "type": "boolean",
                    "description": "Include parent, children, citations, and terms (default true)",
                    "default": True,
                },
            },
            "required": ["ids"],
        },
    },
    {
        "name": "search",
        "title": "Search",
        "description": "Find propositions, glossary terms, and sections. Words are matched case-insensitively and all must appear. A number like \"6\" or \"6.1\" matches that proposition and its descendants.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_term",
        "title": "Get a glossary term",
        "description": "Return a glossary definition and the full text of the propositions it cites. Accepts the term name or its id from list_terms.",
        "inputSchema": {
            "type": "object",
            "properties": {"term": {"type": "string"}},
            "required": ["term"],
        },
    },
    {
        "name": "list_terms",
        "title": "List glossary terms",
        "description": "List every glossary term with its id.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]

for _tool in TOOLS:
    _tool["annotations"] = {"readOnlyHint": True, "openWorldHint": False}

ABOUT_HEADING_RE = re.compile(r"^## (.+)$", re.M)


def parse_about(text):
    parts = ABOUT_HEADING_RE.split(text or "")
    return {parts[i].strip().lower(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


class Tractate:
    def __init__(self, graph, about_text=""):
        self.graph = graph
        self.about = parse_about(about_text)
        self.meta = graph["meta"]
        self.sections = graph["sections"]
        self.section_by_id = {s["id"]: s for s in self.sections}
        self.props = graph["propositions"]
        self.terms = graph["terms"]
        self.order = graph["order"]
        self.order_index = {pid: i for i, pid in enumerate(self.order)}
        self.chapters = [s for s in self.sections if s["kind"] == "chapter"]
        self.full_text = self.render_full()

    @property
    def title(self):
        return self.meta.get("title") or "Tractate"

    def byline(self):
        return ", ".join(b for b in (self.meta.get("author"), self.meta.get("date")) if b)

    @property
    def subtitle(self):
        return self.about.get("subtitle", "")

    @property
    def full_title(self):
        return f"{self.title}: {self.subtitle}" if self.subtitle else self.title

    def format_line(self):
        who = f" by {self.meta['author']}" if self.meta.get("author") else ""
        when = f" ({self.meta['date']})" if self.meta.get("date") else ""
        return (
            f"{self.title}{who}{when} is written as {len(self.order)} numbered propositions "
            f"across {len(self.chapters)} chapters, with a glossary of {len(self.terms)} terms. "
            "Propositions cite one another by number, so the text forms a citation graph."
        )

    def live_count(self, text):
        return STATED_COUNT_RE.sub(str(len(self.order)), text or "")

    def summary(self):
        return self.live_count(self.about.get("summary") or self.format_line())

    def short_description(self):
        return self.live_count(self.about.get("short description") or self.summary())

    def about_markdown(self, level=2, lead=True):
        h = "#" * level
        parts = [f"{h} About this work (the author's summary)", self.summary(), self.format_line()] if lead else []
        for key, label in (
            ("author's note", "A note from the author"),
            ("where to start", "Where to start"),
            ("guidance for assistants", "For AI assistants"),
            ("example questions", "Questions people ask"),
            ("themes", "Themes"),
        ):
            if self.about.get(key):
                parts.append(f"{h} {label}\n\n{self.about[key]}")
        return "\n\n".join(parts)

    def llms_full(self):
        head = f"# {self.full_title}\n\n{self.byline()}\n\n"
        return head + self.about_markdown() + "\n\n---\n\n" + self.full_text

    def section_label(self, s):
        return f"{s['number']}. {s['title']}" if s["kind"] == "chapter" else s["title"]

    def render_section(self, s):
        out = []
        if s["kind"] == "chapter":
            out.append(f"## {s['number']}. {s['title']}")
            for b in s["blocks"]:
                if b["type"] == "heading":
                    out.append(f"### {b['text']}")
                elif b["type"] == "prose":
                    out.append(b["text"])
                elif b["type"] == "proposition":
                    out.append(f"**{b['id']}** {self.props[b['id']]['text']}")
        elif s["kind"] == "glossary":
            out.append(f"## {s['title']}")
            out += [b["text"] for b in s["blocks"] if b["type"] == "prose"]
            for tid in s["termIds"]:
                t = self.terms[tid]
                out.append(f"**{t['term']}**: {t['text']}")
        else:
            out.append(f"## {s['title']}")
            out += [b["text"] for b in s["blocks"]]
        return "\n\n".join(out)

    def render_full(self):
        head = [f"# {self.title}"]
        if self.byline():
            head.append(self.byline())
        return "\n\n".join(head + [self.render_section(s) for s in self.sections]) + "\n"

    def section_lines(self):
        lines = []
        for s in self.sections:
            if s["kind"] == "chapter":
                extra = f" ({len(s['propositionIds'])} propositions)"
            elif s["kind"] == "glossary":
                extra = f" ({len(s['termIds'])} terms)"
            else:
                extra = ""
            lines.append(f"- `{s['id']}`: {self.section_label(s)}{extra}")
        return lines

    def numbering_notes(self):
        return [
            "Propositions are numbered `chapter.decimal` (e.g. `3.02`) and read in document order.",
            "A proposition's parent is found by dropping trailing digits: `1.611` elaborates `1.61`, which elaborates `1.6`.",
            "Propositions cite each other by number in their text (single ids or ranges like `3.0–3.3`); citations are resolved in both directions (cites / cited by).",
            "Glossary terms cite the propositions that define or use them.",
        ]

    def overview(self):
        parts = [f"# {self.full_title}"]
        if self.byline():
            parts.append(self.byline())
        parts.append(self.about_markdown())
        parts.append("## How it is organized\n\n" + "\n".join("- " + n for n in self.numbering_notes()))
        parts.append("## Sections\n\n" + "\n".join(self.section_lines()))
        return "\n\n".join(parts)

    def find_section(self, ref):
        q = str(ref).strip()
        low = q.lower().rstrip(".")
        if low in self.section_by_id:
            return self.section_by_id[low]
        if slug(q) in self.section_by_id:
            return self.section_by_id[slug(q)]
        for s in self.sections:
            if s["title"].lower() == low or self.section_label(s).lower() == q.lower():
                return s
        for s in self.sections:
            if low and low in s["title"].lower():
                return s
        return None

    def find_term(self, ref):
        q = str(ref).strip()
        low = q.lower().strip('"')
        if slug(q) in self.terms:
            return self.terms[slug(q)]
        for t in self.terms.values():
            if t["term"].lower().strip('"') == low:
                return t
        for t in self.terms.values():
            if low and low in t["term"].lower():
                return t
        return None

    def expand_ids(self, ids):
        out = []
        missing = []
        for raw in ids:
            ref = str(raw).strip()
            m = RANGE_ID_RE.match(ref)
            if m and m.group(1) in self.order_index and m.group(2) in self.order_index:
                i, j = sorted((self.order_index[m.group(1)], self.order_index[m.group(2)]))
                out += self.order[i : j + 1]
            elif ref in self.props:
                out.append(ref)
            else:
                missing.append(ref)
        seen = set()
        uniq = [p for p in out if not (p in seen or seen.add(p))]
        return uniq, missing

    def prop_ref(self, pid):
        p = self.props.get(pid)
        return f"- {pid}: {clip(p['text'])}" if p else f"- {pid} (missing)"

    def render_prop(self, pid, related):
        p = self.props[pid]
        chap = self.section_by_id[p["chapter"]]
        out = [f"## {pid}", f"Chapter {self.section_label(chap)}", p["text"]]
        if not related:
            return "\n\n".join(out)
        out.append("Parent:\n" + (self.prop_ref(p["parent"]) if p["parent"] else "- none (top level of chapter)"))
        for label, key in (("Children", "children"), ("Cites", "cites"), ("Cited by", "citedBy")):
            items = p[key]
            out.append(f"{label}:\n" + ("\n".join(self.prop_ref(c) for c in items) if items else "- none"))
        if p["terms"]:
            out.append("Glossary terms:\n" + "\n".join(f"- {self.terms[t]['term']} (`{t}`)" for t in p["terms"]))
        if p["unresolved"]:
            out.append("Unresolved references: " + ", ".join(p["unresolved"]))
        return "\n\n".join(out)

    def get_propositions(self, ids, related):
        if isinstance(ids, str):
            ids = [ids]
        found, missing = self.expand_ids(ids)
        if not found:
            return None, "No propositions found for: " + ", ".join(missing)
        truncated = len(found) > MAX_IDS
        found = found[:MAX_IDS]
        body = "\n\n---\n\n".join(self.render_prop(pid, related) for pid in found)
        notes = []
        if missing:
            notes.append("Not found: " + ", ".join(missing))
        if truncated:
            notes.append(f"Truncated to the first {MAX_IDS} propositions.")
        return body + ("\n\n" + "\n".join(notes) if notes else ""), None

    def term_text(self, t):
        out = [f"## {t['term']}", f"id: `{t['id']}`", t["text"]]
        if t["cites"]:
            out.append("Cited propositions:\n\n" + "\n\n".join(f"**{c}** {self.props[c]['text']}" for c in t["cites"]))
        if t["unresolved"]:
            out.append("Unresolved references: " + ", ".join(t["unresolved"]))
        return "\n\n".join(out)

    def search(self, query, limit):
        q = " ".join(str(query).lower().split())
        if not q:
            return None, "Empty query."
        words = q.split()
        hits = []
        if NUM_RE.match(q):
            for s in self.chapters:
                if str(s["number"]) == q:
                    hits.append(f"- section `{s['id']}`: {self.section_label(s)}")
            for pid in self.order:
                ok = pid == q or pid.startswith(q) if "." in q else pid == q or pid.startswith(q + ".")
                if ok:
                    hits.append(f"- proposition {pid}: {clip(self.props[pid]['text'])}")
            for t in self.terms.values():
                if any(c == q or c.startswith(q + ".") for c in t["cites"]):
                    hits.append(f"- term `{t['id']}` {t['term']}: {clip(t['text'])}")
        else:
            for s in self.sections:
                if all(w in s["title"].lower() for w in words):
                    hits.append(f"- section `{s['id']}`: {self.section_label(s)}")
            for t in self.terms.values():
                hay = (t["term"] + " " + t["text"]).lower()
                if all(w in hay for w in words):
                    hits.append(f"- term `{t['id']}` {t['term']}: {around(t['text'], words[0])}")
            for pid in self.order:
                text = self.props[pid]["text"]
                if all(w in text.lower() for w in words):
                    hits.append(f"- proposition {pid}: {around(text, words[0])}")
        if not hits:
            return f"No matches for \"{query}\".", None
        shown = hits[:limit]
        tail = f"\n\n{len(hits) - len(shown)} more matches not shown." if len(hits) > len(shown) else ""
        return f"{len(hits)} matches for \"{query}\":\n\n" + "\n".join(shown) + tail, None

    def call_tool(self, name, args):
        if name == "get_overview":
            return self.overview(), None
        if name == "read_full":
            return self.full_text, None
        if name == "read_section":
            s = self.find_section(args.get("section", ""))
            if not s:
                return None, "Unknown section. Valid ids:\n" + "\n".join(self.section_lines())
            return self.render_section(s), None
        if name == "get_propositions":
            return self.get_propositions(args.get("ids") or [], args.get("include_related", True) is not False)
        if name == "search":
            try:
                limit = max(1, min(100, int(args.get("limit", 20))))
            except (TypeError, ValueError):
                limit = 20
            return self.search(args.get("query", ""), limit)
        if name == "get_term":
            t = self.find_term(args.get("term", ""))
            if not t:
                return None, "Unknown term. Use list_terms to see all terms."
            return self.term_text(t), None
        if name == "list_terms":
            return "\n".join(f"- `{t['id']}`: {t['term']}" for t in self.terms.values()), None
        raise RpcError(-32602, f"Unknown tool: {name}")

    def resources(self):
        items = [
            {
                "uri": "tractate://full",
                "name": "full",
                "title": f"{self.title} (full text)",
                "description": "The entire tractate as Markdown.",
                "mimeType": "text/markdown",
                "size": len(self.full_text.encode("utf-8")),
            }
        ]
        for s in self.sections:
            items.append(
                {
                    "uri": f"tractate://section/{s['id']}",
                    "name": f"section-{s['id']}",
                    "title": self.section_label(s),
                    "mimeType": "text/markdown",
                }
            )
        return items

    def read_resource(self, uri):
        if uri == "tractate://full":
            text = self.full_text
        elif uri.startswith("tractate://section/") and uri[19:] in self.section_by_id:
            text = self.render_section(self.section_by_id[uri[19:]])
        else:
            raise RpcError(-32002, f"Resource not found: {uri}")
        return {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": text}]}

    def instructions(self):
        tools = (
            "Tools: get_overview for the summary, themes, and section ids; read_full for everything; "
            "read_section for one chapter; get_propositions for numbered propositions and their citation neighborhood; "
            "search to locate passages; get_term for glossary definitions."
        )
        parts = [
            f"Read-only access to \"{self.full_title}\"{' by ' + self.meta['author'] if self.meta.get('author') else ''}.",
            "About this work (the author's summary): " + self.summary(),
        ]
        if self.about.get("guidance for assistants"):
            parts.append("How to help users with it:\n" + self.about["guidance for assistants"])
        parts.append(tools)
        return "\n\n".join(parts)

    def dispatch(self, method, params):
        if method == "initialize":
            asked = params.get("protocolVersion")
            return {
                "protocolVersion": asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"listChanged": False, "subscribe": False},
                },
                "serverInfo": {"name": "tractate", "title": self.title, "version": SERVER_VERSION},
                "instructions": self.instructions(),
            }
        if method == "ping":
            return {}
        if method == "tools/list":
            return {"tools": TOOLS}
        if method == "tools/call":
            args = params.get("arguments") or {}
            if not isinstance(args, dict):
                raise RpcError(-32602, "arguments must be an object")
            text, err = self.call_tool(params.get("name"), args)
            if err:
                return {"content": [{"type": "text", "text": err}], "isError": True}
            return {"content": [{"type": "text", "text": text}]}
        if method == "resources/list":
            return {"resources": self.resources()}
        if method == "resources/templates/list":
            return {
                "resourceTemplates": [
                    {
                        "uriTemplate": "tractate://section/{id}",
                        "name": "section",
                        "title": "Section by id",
                        "description": "A chapter number, \"preface\", \"glossary\", or another section id from get_overview.",
                        "mimeType": "text/markdown",
                    }
                ]
            }
        if method == "resources/read":
            return self.read_resource(str(params.get("uri", "")))
        if method == "prompts/list":
            return {"prompts": []}
        raise RpcError(-32601, f"Method not found: {method}")

    def handle(self, msg):
        if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
            return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        if "method" not in msg:
            return None
        is_note = "id" not in msg
        params = msg.get("params") or {}
        if not isinstance(params, dict):
            params = {}
        try:
            result = self.dispatch(msg["method"], params)
        except RpcError as e:
            if is_note:
                return None
            return {"jsonrpc": "2.0", "id": msg["id"], "error": {"code": e.code, "message": e.message}}
        if is_note:
            return None
        return {"jsonrpc": "2.0", "id": msg["id"], "result": result}

    def llms_txt(self, base):
        tool_lines = "\n".join(f"- `{t['name']}`: {t['description']}" for t in TOOLS)
        section_links = "\n".join(
            f"- [{self.section_label(s)}]({base}/#{s['id']}): section id `{s['id']}`" for s in self.sections
        )
        notes = "\n".join("- " + n for n in self.numbering_notes())
        return f"""# {self.full_title}

> {self.summary()}

That is the author's own summary. {self.format_line()}

Start here: this file describes the work, how to help someone who asks about it, and every way to read it. To read the whole work, fetch {base}/llms-full.txt. To explore it selectively, connect to the MCP server at {base}/mcp and call `get_overview`. The homepage {base}/ also contains the complete text as plain HTML; no JavaScript is required.

{self.about_markdown(lead=False)}

## MCP server

- Endpoint: {base}/mcp
- Transport: Streamable HTTP. JSON-RPC 2.0 over POST, JSON responses, stateless, no authentication, read-only.
- Protocol versions: {", ".join(PROTOCOL_VERSIONS)}

Client configuration:

```json
{{"mcpServers": {{"tractate": {{"url": "{base}/mcp"}}}}}}
```

Tools:

{tool_lines}

Resources:

- `tractate://full`: the entire tractate as Markdown
- `tractate://section/{{id}}`: one section by id (chapter number, `preface`, `glossary`, ...)

## Plain text

- [Full text]({base}/llms-full.txt): the complete tractate as Markdown
- [Reader]({base}/): interactive reader with a citation graph; link to a proposition with `{base}/#3.02`, a chapter with `{base}/#3`, a term with `{base}/#glossary/<term-id>`

## Structure

{notes}

## Sections

{section_links}

## License

Copyright (c) {self.meta.get("date") or ""} {self.meta.get("author") or ""}. All rights reserved, with permission to read, share, quote, adapt, and build upon this material provided that: any use explicitly names the author and the work and links to the original repository ({SOURCE_URL}); adapted material says it is adapted and links to the original; no endorsement by the author is implied; and redistributions include the license. Full terms: {SOURCE_URL}/blob/main/LICENSE.txt

Source: {SOURCE_URL}
"""
