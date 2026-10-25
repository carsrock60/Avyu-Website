"""Local static server and bot API. Run with: python3 server.py"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from bot_logic import choose_move, validate_request

ROOT = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path != "/api/bot-move":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 4096:
                raise ValueError("Invalid request size")
            payload = json.loads(self.rfile.read(length))
            board, player, difficulty = validate_request(payload)
            self._send_json(200, {"move": choose_move(board, player, difficulty)})
        except (KeyError, TypeError, ValueError) as error:
            self._send_json(400, {"error": str(error)})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print(f"Tic tac toe is ready at http://{address[0]}:{address[1]}")
    ThreadingHTTPServer(address, Handler).serve_forever()
