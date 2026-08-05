from __future__ import annotations

import json
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from outputs.feed_air_server import parse_uploaded_file


ROOT = Path(__file__).resolve().parent.parent


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/", "/outputs/feed-air-calculator.html"}:
            html_path = ROOT / "outputs" / "feed-air-calculator.html"
            data = html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404, "Not found")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:
        try:
            filename, data = self._read_uploaded_file()
            rows = parse_uploaded_file(filename, data)
            self._send_json({"ok": True, "filename": filename, "rows": rows})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=400)

    def _read_uploaded_file(self) -> tuple[str, bytes]:
        content_type = self.headers.get("Content-Type", "")
        content_length = int(self.headers.get("Content-Length", "0") or 0)
        if content_length <= 0:
            raise ValueError("No uploaded file was received.")
        body = self.rfile.read(content_length)
        raw = (
            f"Content-Type: {content_type}\r\n"
            "MIME-Version: 1.0\r\n\r\n"
        ).encode("utf-8") + body
        message = BytesParser(policy=policy.default).parsebytes(raw)
        if not message.is_multipart():
            raise ValueError("Upload request must be multipart/form-data.")

        for part in message.iter_parts():
            if part.get_content_disposition() != "form-data":
                continue
            if part.get_param("name", header="content-disposition") != "file":
                continue
            filename = part.get_filename() or "upload"
            payload = part.get_payload(decode=True)
            if not payload:
                raise ValueError("Uploaded file is empty.")
            return filename, payload
        raise ValueError("Could not find the uploaded file field.")

    def _send_json(self, payload: dict, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
