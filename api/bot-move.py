"""Vercel serverless endpoint for bot moves."""
from http.server import BaseHTTPRequestHandler
import json

from bot_logic import choose_move, validate_request


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 4096:
                raise ValueError("Invalid request size")
            payload = json.loads(self.rfile.read(length))
            board, player, difficulty = validate_request(payload)
            response = {"move": choose_move(board, player, difficulty)}
            self._send_json(200, response)
        except (KeyError, TypeError, ValueError) as error:
            self._send_json(400, {"error": str(error)})

    def do_OPTIONS(self):
        self._send_json(204, {})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body)


if __name__ == "__main__":
    from http.server import HTTPServer
    HTTPServer(("127.0.0.1", 8000), handler).serve_forever()
