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

    def md(self, text):
        out = []
        for block in re.split(r"\n\s*\n", (text or "").strip()):
            lines = [l for l in block.splitlines() if l.strip()]
            if not lines:
                continue
            if lines[0].lstrip().startswith("- "):
                out.append(self.md_list(lines))
            else:
                out.append(f"<p>{self.inline(' '.join(l.strip() for l in lines))}</p>")
        return "\n".join(out)

    def md_list(self, lines):
        html = []
        stack = []
        for line in lines:
            indent = len(line) - len(line.lstrip())
            text = line.strip()
            item = text[2:] if text.startswith("- ") else text
            while stack and indent < stack[-1]:
                stack.pop()
                html.append("</ul></li>")
            if not stack or indent > stack[-1]:
                if stack and html[-1].endswith("</li>"):
                    html[-1] = html[-1][:-5]
                html.append("<ul>")
                stack.append(indent)
            html.append(f"<li>{self.inline(item)}</li>")
        while stack:
            stack.pop()
            html.append("</ul></li>" if stack else "</ul>")
        return "".join(html)

    def description(self):
        return self.t.short_description()

    def head(self, base):
        t = self.t
        desc = attr(self.description())
        return "\n".join(
            [
                f"<title>{esc(t.full_title)}</title>",
                f'<meta name="description" content="{desc}">',
                f'<meta property="og:title" content="{attr(t.full_title)}">',
                f'<meta property="og:description" content="{desc}">',
                f'<meta property="og:url" content="{attr(base)}/">',
                '<meta property="og:type" content="article">',
                '<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">',
                '<link rel="alternate" type="text/plain" href="/llms-full.txt" title="llms-full.txt">',
            ]
        )

    def about_html(self, base):
        t = self.t
        out = [
            f"<h1>{esc(t.title)}</h1>",
            f"<p><em>{esc(t.subtitle)}</em></p>" if t.subtitle else "",
            f"<p>{esc(t.byline())} · {esc(domain(base))}</p>",
            "<h2>About this work (the author's summary)</h2>",
            f"<p>{self.inline(t.summary())}</p>",
            f"<p>{esc(t.format_line())}</p>",
        ]
        for key, label in (
            ("where to start", "Where to start"),
            ("guidance for assistants", "For AI assistants"),
            ("example questions", "Questions people ask"),
            ("themes", "Themes"),
        ):
            if t.about.get(key):
                out.append(f"<h2>{label}</h2>")
                out.append(self.md(t.about[key]))
        return "\n".join(x for x in out if x)

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
                "<h2>Reading this with tools</h2>",
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
        body = "\n".join(
            [self.about_html(base), self.agent_block(base)] + [self.section_html(s) for s in self.t.sections]
        )
        return (
            self.template.replace("{{head}}", self.head(base))
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
