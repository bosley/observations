#!/usr/bin/env python3
import argparse
import json
import mimetypes
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from mcp_server import Tractate
from pages import Pages
from parse import parse

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
DEFAULT_MD = ROOT.parent / "tractate.md"
MAX_BODY = 1 << 20


class Handler(BaseHTTPRequestHandler):
    graph_json = b"{}"
    tractate = None
    pages = None
    base_url = ""
    head_only = False

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _base(self):
        if Handler.base_url:
            return Handler.base_url
        proto = (self.headers.get("X-Forwarded-Proto") or "http").split(",")[0].strip()
        host = (self.headers.get("X-Forwarded-Host") or self.headers.get("Host") or "").split(",")[0].strip()
        if not host:
            host = "%s:%d" % self.server.server_address[:2]
        return "%s://%s" % (proto, host)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Accept, Authorization, Mcp-Session-Id, Mcp-Protocol-Version, Last-Event-ID",
        )
        self.send_header("Access-Control-Expose-Headers", "Mcp-Session-Id")

    def _agent_link(self):
        self.send_header(
            "Link",
            '</llms.txt>; rel="alternate"; type="text/plain"; title="llms.txt", '
            '</llms-full.txt>; rel="alternate"; type="text/plain"; title="llms-full.txt"',
        )

    def _send_bytes(self, status, data, ctype, link=False):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        if link:
            self._agent_link()
        self._cors()
        self.end_headers()
        if not self.head_only:
            self.wfile.write(data)

    def _not_found(self):
        html = Handler.pages.not_found(self._base(), urlparse(self.path).path)
        self._send_bytes(404, html.encode("utf-8"), "text/html; charset=utf-8", link=True)

    def do_HEAD(self):
        self.head_only = True
        self.do_GET()

    def _send_json(self, status, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send_bytes(status, data, "application/json; charset=utf-8")

    def _send_empty(self, status, extra=None):
        self.send_response(status)
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", "0")
        self._cors()
        self.end_headers()

    def do_OPTIONS(self):
        self._send_empty(204, {"Access-Control-Max-Age": "86400"})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path in ("/", "/index.html"):
            html = Handler.pages.index(self._base())
            self._send_bytes(200, html.encode("utf-8"), "text/html; charset=utf-8", link=True)
            return
        if path == "/robots.txt":
            self._send_bytes(200, Handler.pages.robots(self._base()).encode("utf-8"), "text/plain; charset=utf-8")
            return
        if path == "/api/graph":
            self._send_bytes(200, Handler.graph_json, "application/json; charset=utf-8")
            return
        if path == "/llms.txt":
            text = Handler.tractate.llms_txt(self._base())
            self._send_bytes(200, text.encode("utf-8"), "text/plain; charset=utf-8")
            return
        if path == "/llms-full.txt":
            self._send_bytes(200, Handler.tractate.full_text.encode("utf-8"), "text/plain; charset=utf-8")
            return
        if path == "/mcp":
            self._send_empty(405, {"Allow": "POST, OPTIONS"})
            return
        if path.startswith("/static/"):
            rel = path[len("/static/") :]
            target = (STATIC / rel).resolve()
            if not str(target).startswith(str(STATIC.resolve())) or not target.is_file():
                self._not_found()
                return
            self._send_file(target)
            return
        self._not_found()

    def do_DELETE(self):
        if urlparse(self.path).path == "/mcp":
            self._send_empty(405, {"Allow": "POST, OPTIONS"})
            return
        self._not_found()

    def do_POST(self):
        if urlparse(self.path).path != "/mcp":
            self._not_found()
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if length < 0 or length > MAX_BODY:
            self._send_json(413, {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Request too large"}})
            return
        try:
            msg = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._send_json(400, {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
            return
        t = Handler.tractate
        if isinstance(msg, list):
            replies = [r for r in (t.handle(m) for m in msg) if r is not None]
            if replies:
                self._send_json(200, replies)
            else:
                self._send_empty(202)
            return
        reply = t.handle(msg)
        if reply is None:
            self._send_empty(202)
        else:
            self._send_json(200, reply)

    def _send_file(self, path):
        data = path.read_bytes()
        ctype, _ = mimetypes.guess_type(str(path))
        if ctype is None:
            ctype = "application/octet-stream"
        if ctype.startswith("text/") or ctype in (
            "application/javascript",
            "application/json",
        ):
            ctype = ctype + "; charset=utf-8"
        if path.suffix == ".js":
            ctype = "text/javascript; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if not self.head_only:
            self.wfile.write(data)


def main():
    parser = argparse.ArgumentParser(description="Browse a tractate locally.")
    parser.add_argument(
        "markdown",
        nargs="?",
        default=str(DEFAULT_MD),
        help="path to tractate markdown (default: ../tractate.md)",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--base-url",
        default="",
        help="public URL used in llms.txt, e.g. https://beausol.ai (default: from request headers)",
    )
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    md = Path(args.markdown).resolve()
    if not md.is_file():
        sys.stderr.write("no such file: %s\n" % md)
        sys.exit(1)
    graph = parse(md)
    text = json.dumps(graph, ensure_ascii=False)
    Handler.graph_json = text.encode("utf-8")
    Handler.tractate = Tractate(graph)
    Handler.pages = Pages(Handler.tractate, (STATIC / "index.html").read_text(encoding="utf-8"))
    Handler.base_url = args.base_url.rstrip("/")
    nprop = len(graph["propositions"])
    nterm = len(graph["terms"])
    url = "http://%s:%d" % (args.host, args.port)
    print("parsed %s" % md, flush=True)
    print("%d propositions, %d terms" % (nprop, nterm), flush=True)
    print("serving %s" % url, flush=True)
    print("mcp at %s/mcp, agent index at %s/llms.txt" % (url, url), flush=True)
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
