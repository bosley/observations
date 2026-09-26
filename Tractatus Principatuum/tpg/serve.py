#!/usr/bin/env python3
import argparse
import json
import mimetypes
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from parse import parse

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
DEFAULT_MD = ROOT.parent / "tractate.md"


class Handler(BaseHTTPRequestHandler):
    graph_json = b"{}"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/":
            self._send_file(STATIC / "index.html")
            return
        if path == "/api/graph":
            data = Handler.graph_json
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(data)
            return
        if path.startswith("/static/"):
            rel = path[len("/static/") :]
            target = (STATIC / rel).resolve()
            if not str(target).startswith(str(STATIC.resolve())) or not target.is_file():
                self.send_error(404)
                return
            self._send_file(target)
            return
        self.send_error(404)

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
        self.wfile.write(data)


def main():
    parser = argparse.ArgumentParser(description="Browse a tractate locally.")
    parser.add_argument(
        "markdown",
        nargs="?",
        default=str(DEFAULT_MD),
        help="path to tractate markdown (default: ../tractate.md)",
    )
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    md = Path(args.markdown).resolve()
    if not md.is_file():
        sys.stderr.write("no such file: %s\n" % md)
        sys.exit(1)
    graph = parse(md)
    text = json.dumps(graph, ensure_ascii=False)
    Handler.graph_json = text.encode("utf-8")
    nprop = len(graph["propositions"])
    nterm = len(graph["terms"])
    url = "http://127.0.0.1:%d" % args.port
    print("parsed %s" % md, flush=True)
    print("%d propositions, %d terms" % (nprop, nterm), flush=True)
    print("serving %s" % url, flush=True)
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        HTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
