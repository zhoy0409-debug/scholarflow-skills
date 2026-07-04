#!/usr/bin/env python3
"""Serve the storage report with a guarded local action API."""

from __future__ import annotations

import json
import os
import secrets
import shutil
import subprocess
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "report_template.html")
HOME = os.path.realpath(os.path.expanduser("~"))
TOKEN = secrets.token_urlsafe(24)

DATA: dict = {}
TPL = ""
RM_ALLOW: set[str] = set()
TRASH_ALLOW: set[str] = set()
OPEN_ALLOW: set[str] = set()


def expand(path: str) -> str:
    return os.path.realpath(os.path.expanduser(path))


def load(src: str):
    with open(src, encoding="utf-8") as handle:
        data = json.load(handle)
    with open(TEMPLATE, encoding="utf-8") as handle:
        template = handle.read()
    rm_allow: set[str] = set()
    trash_allow: set[str] = set()
    open_allow: set[str] = set()
    for item in data.get("green", []):
        for raw in item.get("trash_paths") or []:
            path = expand(raw)
            rm_allow.add(path)
            trash_allow.add(path)
            open_allow.add(path)
    for item in data.get("yellow", []):
        for raw in item.get("trash_paths") or []:
            path = expand(raw)
            trash_allow.add(path)
            open_allow.add(path)
        if item.get("path"):
            path = expand(item["path"])
            if os.path.exists(path):
                open_allow.add(path)
    for item in data.get("red", []):
        for raw in item.get("app_paths") or []:
            path = expand(raw)
            if os.path.exists(path):
                open_allow.add(path)
    return data, template, rm_allow, trash_allow, open_allow


def move_to_trash(path: str) -> None:
    if sys.platform == "darwin":
        script = 'tell application "Finder" to delete (POSIX file %s as alias)' % json.dumps(path)
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode != 0:
            destination = os.path.join(HOME, ".Trash", os.path.basename(path.rstrip("/")) + "." + time.strftime("%H%M%S"))
            shutil.move(path, destination)
    elif sys.platform.startswith("win"):
        import ctypes
        from ctypes import wintypes

        class SHFILEOPSTRUCTW(ctypes.Structure):
            _fields_ = [
                ("hwnd", wintypes.HWND),
                ("wFunc", wintypes.UINT),
                ("pFrom", wintypes.LPCWSTR),
                ("pTo", wintypes.LPCWSTR),
                ("fFlags", ctypes.c_uint16),
                ("fAnyOperationsAborted", wintypes.BOOL),
                ("hNameMappings", ctypes.c_void_p),
                ("lpszProgressTitle", wintypes.LPCWSTR),
            ]

        op = SHFILEOPSTRUCTW()
        op.wFunc = 3
        op.pFrom = os.path.abspath(path) + "\x00\x00"
        op.fFlags = 0x0040 | 0x0010 | 0x0004
        rc = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
        if rc != 0:
            raise OSError(f"SHFileOperation failed with code {rc}")
    else:
        raise OSError("Trash action is supported only on macOS and Windows.")


def hard_delete(path: str) -> None:
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def open_in_file_manager(path: str) -> None:
    target = path if os.path.isdir(path) else os.path.dirname(path)
    if sys.platform == "darwin":
        result = subprocess.run(["open", target], capture_output=True, text=True)
        if result.returncode != 0:
            result = subprocess.run(["open", "-R", target], capture_output=True, text=True)
        if result.returncode != 0:
            raise OSError((result.stderr or "open failed").strip())
    elif sys.platform.startswith("win"):
        subprocess.run(["explorer", target], check=False)
    else:
        raise OSError("Open action is supported only on macOS and Windows.")


def allowed(path: str, allowlist: set[str]) -> bool:
    real = expand(path)
    return real in allowlist and (real == HOME or real.startswith(HOME + os.sep))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        return None

    def _send(self, code: int, body, content_type: str = "application/json") -> None:
        payload = body.encode("utf-8") if isinstance(body, str) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            blob = json.dumps(DATA, ensure_ascii=False)
            cfg = json.dumps({"token": TOKEN, "endpoint": "/action"})
            html = TPL.replace("__REPORT_DATA__", blob).replace("__DELETE_CONFIG__", cfg)
            self._send(200, html, "text/html; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/action":
            self._send(404, {"ok": False, "error": "not found"})
            return
        if self.headers.get("X-Storage-Token") != TOKEN:
            self._send(403, {"ok": False, "error": "invalid token"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        action = request.get("action")
        path = expand(request.get("path", ""))
        try:
            if action == "trash":
                if not allowed(path, TRASH_ALLOW):
                    raise PermissionError("path is not allowed for trash")
                move_to_trash(path)
            elif action == "rm":
                if not allowed(path, RM_ALLOW):
                    raise PermissionError("path is not allowed for delete")
                hard_delete(path)
            elif action == "open":
                if not allowed(path, OPEN_ALLOW):
                    raise PermissionError("path is not allowed for open")
                open_in_file_manager(path)
            else:
                raise ValueError("unknown action")
        except Exception as exc:
            self._send(400, {"ok": False, "error": str(exc)})
            return
        self._send(200, {"ok": True, "action": action, "path": path})


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: server.py <analysis.json>")
        return 2
    global DATA, TPL, RM_ALLOW, TRASH_ALLOW, OPEN_ALLOW
    DATA, TPL, RM_ALLOW, TRASH_ALLOW, OPEN_ALLOW = load(sys.argv[1])
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"Storage report server: {url}")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
