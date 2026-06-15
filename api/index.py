"""
Vercel serverless adapter for LatentSearch.

vercel.json rewrites every /api/* request to /api/index?path=<segments>.
This handler reconstructs the original path from that query parameter and
then delegates to the existing LatentSearchHandler logic in server.py.
Static files are served directly by Vercel's CDN.
"""

import os
import sys
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

# Make the project root importable so we can reuse server.py logic.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import LatentSearchHandler, load_local_env  # noqa: E402

# Ensure any local .env is loaded (harmless on Vercel, where env vars are
# injected directly into the runtime environment).
load_local_env()


def _reconstruct_path(path: str) -> str:
    """
    Reverse the Vercel rewrite.

    Input : "/api/index?path=images%2Fstream&query=cat"
    Output: "/api/images/stream?query=cat"
    """
    parsed = urlparse(path)
    params = parse_qs(parsed.query, keep_blank_values=True)
    segments = params.pop("path", [""])[0].lstrip("/")

    new_query = urlencode(params, doseq=True)
    new_path = f"/api/{segments}" if segments else "/api"
    return urlunparse(parsed._replace(path=new_path, query=new_query))


class handler(LatentSearchHandler):
    """Vercel-compatible handler that exposes only the /api/* endpoints."""

    def _prepare(self):
        # Undo the rewrite so server.py sees the original request path.
        self.path = _reconstruct_path(self.path)

    def do_GET(self):
        self._prepare()
        if self.path.startswith("/api/"):
            super().do_GET()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        self._prepare()
        if self.path.startswith("/api/"):
            super().do_POST()
        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        self._prepare()
        if self.path.startswith("/api/"):
            super().do_OPTIONS()
        else:
            self.send_error(404, "Not Found")
