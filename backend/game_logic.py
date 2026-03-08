"""
game_logic.py - Core game logic for Tic-Tac-Toe
Handles board representation, move validation, win/draw detection, and turn switching.
"""

from typing import Optional

# Board is a list of 9 elements: 'X', 'O', or None
Board = list[Optional[str]]

WIN_COMBINATIONS = [
    [0, 1, 2],  # top row
    [3, 4, 5],  # middle row
    [6, 7, 8],  # bottom row
    [0, 3, 6],  # left column
    [1, 4, 7],  # middle column
    [2, 5, 8],  # right column
    [0, 4, 8],  # diagonal
    [2, 4, 6],  # anti-diagonal
]


def create_empty_board() -> Board:
    """Returns a fresh empty board."""
    return [None] * 9


def get_available_moves(board: Board) -> list[int]:
    """Returns list of indices where moves can be made."""
    return [i for i, cell in enumerate(board) if cell is None]


def is_valid_move(board: Board, index: int) -> bool:
    """Check if a move at given index is valid."""
    return 0 <= index < 9 and board[index] is None


def make_move(board: Board, index: int, player: str) -> Board:
    """Apply a move and return new board state (immutable)."""
    new_board = board.copy()
    new_board[index] = player
    return new_board


def check_winner(board: Board) -> Optional[str]:
    """
    Returns 'X' or 'O' if there's a winner, None otherwise.
    """
    for combo in WIN_COMBINATIONS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def get_winning_line(board: Board) -> Optional[list[int]]:
    """Returns the winning combination indices, or None."""
    for combo in WIN_COMBINATIONS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return combo
    return None


def is_draw(board: Board) -> bool:
    """Returns True if the game is a draw (no winner, no moves left)."""
    return check_winner(board) is None and len(get_available_moves(board)) == 0


def is_game_over(board: Board) -> bool:
    """Returns True if the game has ended (win or draw)."""
    return check_winner(board) is not None or is_draw(board)


def get_opponent(player: str) -> str:
    """Returns the opposing player symbol."""
    return 'O' if player == 'X' else 'X'


def get_game_status(board: Board) -> dict:
    """
    Returns a comprehensive game status object.
    """
    winner = check_winner(board)
    draw = is_draw(board)
    winning_line = get_winning_line(board)
    available = get_available_moves(board)

    return {
        "winner": winner,
        "is_draw": draw,
        "is_game_over": winner is not None or draw,
        "winning_line": winning_line,
        "available_moves": available,
        "move_count": 9 - len(available),
    }
