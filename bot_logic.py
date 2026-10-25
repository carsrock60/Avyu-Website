"""Shared tic tac toe bot logic for local and Vercel endpoints."""
import random

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


def choose_move(board, player, difficulty):
    if random.random() < CHANCES[difficulty]:
        return best_move(board, player)
    return random.choice([i for i, value in enumerate(board) if value is None])


def validate_request(payload):
    board = payload["board"]
    player = payload["player"]
    difficulty = payload["difficulty"]
    if (not isinstance(board, list) or len(board) != 9
            or any(value not in (None, "", "x", "o") for value in board)
            or player not in ("x", "o") or difficulty not in CHANCES):
        raise ValueError("Invalid board or bot settings")
    board = [None if value == "" else value for value in board]
    x_count, o_count = board.count("x"), board.count("o")
    if winner(board) or x_count + o_count == 9:
        raise ValueError("The game is already over")
    if (player == "x" and x_count != o_count) or (player == "o" and x_count != o_count + 1):
        raise ValueError("It is not this bot's turn")
    return board, player, difficulty
