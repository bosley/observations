import re
from html import escape
from urllib.parse import urlparse

from mcp_server import TOOLS

INLINE_RE = re.compile(r"`([^`]+)`|(\d+\.\d+)([–-])(\d+\.\d+)|(\d+\.\d+)")


def esc(text):
    return escape(str(text), quote=False)


def attr(text):
    return escape(str(text), quote=True)


def domain(base):
    return urlparse(base).netloc or base


class Pages:
    def __init__(self, tractate, template):
        self.t = tractate
        self.template = template

    def inline(self, text):
        def link(pid):
            cls = "" if pid in self.t.props else ' class="missing"'
            return f'<a href="#{pid}"{cls}>{pid}</a>'

        def sub(m):
            if m.group(1) is not None:
                return f"<code>{m.group(1)}</code>"
            if m.group(2) is not None:
                return link(m.group(2)) + m.group(3) + link(m.group(4))
            return link(m.group(5))

        return INLINE_RE.sub(sub, esc(text))

    def description(self):
        t = self.t
        who = f" by {t.meta['author']}" if t.meta.get("author") else ""
        when = f" ({t.meta['date']})" if t.meta.get("date") else ""
        return (
            f"{t.title}{who}{when}: {len(t.order)} numbered propositions across {len(t.chapters)} chapters, "
            "with a citation graph and glossary. For agents: /llms.txt, full text at /llms-full.txt, MCP server at /mcp."
        )

    def head(self, base):
        t = self.t
        desc = attr(self.description())
        return "\n".join(
            [
                f"<title>{esc(t.title)}</title>",
                f'<meta name="description" content="{desc}">',
                f'<meta property="og:title" content="{attr(t.title)}">',
                f'<meta property="og:description" content="{desc}">',
                f'<meta property="og:url" content="{attr(base)}/">',
                '<meta property="og:type" content="article">',
                '<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">',
                '<link rel="alternate" type="text/plain" href="/llms-full.txt" title="llms-full.txt">',
            ]
        )

    def nav(self):
        out = []
        for s in self.t.sections:
            num = f'<span class="num">{s["number"]}</span> ' if s["kind"] == "chapter" else ""
            out.append(f'<a href="#{attr(s["id"])}">{num}{esc(s["title"])}</a>')
        return "".join(out)

    def agent_block(self, base):
        t = self.t
        mcp = f"{base}/mcp"
        config = f'{{"mcpServers": {{"tractate": {{"url": "{mcp}"}}}}}}'
        tools = "".join(f"<li><code>{esc(x['name'])}</code>: {esc(x['description'])}</li>" for x in TOOLS)
        contents = "".join(
            f'<li><a href="#{attr(s["id"])}">{esc(t.section_label(s))}</a></li>' for s in t.sections
        )
        return "\n".join(
            [
                f"<h1>{esc(t.title)}</h1>",
                f"<p>{esc(t.byline())} · {esc(domain(base))}</p>",
                f"<p>{esc(t.summary())}</p>",
                "<h2>For agents and scripts</h2>",
                "<p>This page is an interactive reader that runs in the browser, but nothing here requires JavaScript. "
                "The complete text is included below this section, and the same material is available in agent-friendly forms:</p>",
                "<ul>",
                f'<li><a href="{attr(base)}/llms.txt">{esc(base)}/llms.txt</a>: start here. Describes the work, its structure, and every way to access it.</li>',
                f'<li><a href="{attr(base)}/llms-full.txt">{esc(base)}/llms-full.txt</a>: the complete tractate as Markdown.</li>',
                f"<li>MCP server at <code>{esc(mcp)}</code>: Streamable HTTP (JSON-RPC 2.0 over POST), stateless, read-only, no authentication. "
                f"Client config: <code>{esc(config)}</code></li>",
                "</ul>",
                "<p>MCP tools:</p>",
                f"<ul>{tools}</ul>",
                "<p>Reader links: a proposition is <code>/#3.02</code>, a chapter is <code>/#3</code>, a glossary term is <code>/#glossary/&lt;term-id&gt;</code>.</p>",
                "<h2>Contents</h2>",
                f"<ul>{contents}</ul>",
            ]
        )

    def section_html(self, s):
        t = self.t
        out = []
        if s["kind"] == "chapter":
            out.append(f'<h2 id="{attr(s["id"])}"><span class="num">{s["number"]}.</span> {esc(s["title"])}</h2>')
            for b in s["blocks"]:
                if b["type"] == "heading":
                    out.append(f"<h3>{esc(b['text'])}</h3>")
                elif b["type"] == "prose":
                    out.append(f"<p>{self.inline(b['text'])}</p>")
                elif b["type"] == "proposition":
                    pid = b["id"]
                    out.append(
                        f'<article class="prop" id="{pid}"><h3><a href="#{pid}">{pid}</a></h3>'
                        f"<p>{self.inline(t.props[pid]['text'])}</p></article>"
                    )
        elif s["kind"] == "glossary":
            out.append(f'<h2 id="glossary">{esc(s["title"])}</h2>')
            out += [f"<p>{self.inline(b['text'])}</p>" for b in s["blocks"] if b["type"] == "prose"]
            for tid in s["termIds"]:
                term = t.terms[tid]
                out.append(
                    f'<article class="term" id="glossary/{attr(tid)}"><h3><a href="#glossary/{attr(tid)}">{esc(term["term"])}</a></h3>'
                    f"<p>{self.inline(term['text'])}</p></article>"
                )
        else:
            out.append(f'<h2 id="{attr(s["id"])}">{esc(s["title"])}</h2>')
            out += [f"<p>{self.inline(b['text'])}</p>" for b in s["blocks"]]
        return "\n".join(out)

    def index(self, base):
        body = self.agent_block(base) + "\n" + "\n".join(self.section_html(s) for s in self.t.sections)
        return (
            self.template.replace("{{head}}", self.head(base))
            .replace("{{nav}}", self.nav())
            .replace("{{read}}", body)
            .replace("{{status}}", esc(f"{len(self.t.order)} propositions · {len(self.t.terms)} terms"))
            .replace("{{byline}}", esc(self.t.byline()))
        )

    def not_found(self, base, path):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Not found: {esc(self.t.title)}</title>
<link rel="stylesheet" href="/static/app.css">
</head>
<body style="overflow:auto">
<main class="read">
<h1>Not found</h1>
<p>Nothing is at <code>{esc(path)}</code>. This site serves {esc(self.t.title)}.</p>
<ul>
<li><a href="{attr(base)}/">{esc(base)}/</a>: the reader</li>
<li><a href="{attr(base)}/llms.txt">{esc(base)}/llms.txt</a>: guide for agents</li>
<li><a href="{attr(base)}/llms-full.txt">{esc(base)}/llms-full.txt</a>: full text as Markdown</li>
<li><code>{esc(base)}/mcp</code>: MCP server (POST, JSON-RPC)</li>
</ul>
</main>
</body>
</html>
"""

    def robots(self, base):
        return f"User-agent: *\nAllow: /\n\n# Agents: see {base}/llms.txt\n"
