"""Local static server and tic tac toe bot endpoint. Run with: python3 server.py"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
CHANCES = {"easy": 0, "medium": 1 / 3, "hard": 2 / 3, "impossible": 1}


def winner(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def minimax(board, player, bot, depth=0):
    result = winner(board)
    if result:
        return (10 - depth) if result == bot else (depth - 10)
    if all(board):
        return 0
    options = []
    for index, value in enumerate(board):
        if value is None:
            next_board = list(board)
            next_board[index] = player
            score = minimax(next_board, "o" if player == "x" else "x", bot, depth + 1)
            options.append(score)
    return max(options) if player == bot else min(options)


def best_move(board, player):
    options = []
    for index, value in enumerate(board):
        if value is None:
            next_board = list(board)
            next_board[index] = player
            score = minimax(next_board, "o" if player == "x" else "x", player, 1)
            options.append((score, index))
    target = max(score for score, _ in options)
    return random.choice([index for score, index in options if score == target])


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
            board = payload["board"]
            player = payload["player"]
            difficulty = payload["difficulty"]
            if (not isinstance(board, list) or len(board) != 9
                    or any(value not in (None, "x", "o") for value in board)
                    or player not in ("x", "o") or difficulty not in CHANCES):
                raise ValueError("Invalid board or bot settings")
            x_count, o_count = board.count("x"), board.count("o")
            if winner(board) or x_count + o_count == 9:
                raise ValueError("The game is already over")
            if (player == "x" and x_count != o_count) or (player == "o" and x_count != o_count + 1):
                raise ValueError("It is not this bot's turn")
            available = [index for index, value in enumerate(board) if value is None]
            if random.random() < CHANCES[difficulty]:
                move = best_move(board, player)
            else:
                move = random.choice(available)
            body = json.dumps({"move": move}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            body = json.dumps({"error": str(error)}).encode()
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print(f"Tic tac toe is ready at http://{address[0]}:{address[1]}")
    ThreadingHTTPServer(address, Handler).serve_forever()
