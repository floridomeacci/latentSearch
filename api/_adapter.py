"""
Shared Vercel adapter for LatentSearch API endpoints.

Adds the project root to sys.path and exposes a handler class that delegates
to the existing LatentSearchHandler from server.py. Individual endpoint files
under api/ import this class as `handler`.
"""

import os
import sys

# Project root is the parent of the api/ directory.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from server import LatentSearchHandler, load_local_env  # noqa: E402

# Ensure any local .env is loaded (harmless on Vercel, where env vars are
# injected directly into the runtime environment).
load_local_env()


class Handler(LatentSearchHandler):
    """Vercel-compatible handler that exposes only the /api/* endpoints."""

    # Static files are served directly by Vercel. If a non-API request reaches
    # this handler, return 404 instead of trying to serve local files.
    def do_GET(self):
        if self.path.startswith("/api/"):
            super().do_GET()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path.startswith("/api/"):
            super().do_POST()
        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        if self.path.startswith("/api/"):
            super().do_OPTIONS()
        else:
            self.send_error(404, "Not Found")
