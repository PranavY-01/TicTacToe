"""
minimax.py - Minimax Algorithm AI
Classic adversarial search with perfect play.

Strategy:
  Explores the entire game tree to find the optimal move.
  Maximizes own score while assuming opponent minimizes it.
  Always plays perfectly - will never lose if a win/draw exists.

Behavior: Unbeatable opponent; always finds optimal outcome.
Difficulty: Hard (optimal play)
"""

from typing import Optional
from game_logic import (
    Board, get_available_moves, make_move, check_winner,
    is_draw, is_game_over, get_opponent
)


def minimax(board: Board, player: str, maximizing_player: str, depth: int = 0) -> int:
    """
    Recursive minimax function.
    
    Args:
        board: Current board state
        player: Whose turn it is right now
        maximizing_player: The AI player (wants to MAXIMIZE score)
        depth: Current recursion depth
    
    Returns:
        Score of the board state from the AI's perspective:
          +10 - depth = AI wins (faster wins score higher)
          -10 + depth = Opponent wins (faster losses score lower)
           0 = Draw
    """
    winner = check_winner(board)
    if winner == maximizing_player:
        return 10 - depth       # AI wins; prefer winning sooner
    if winner is not None:
        return depth - 10       # Opponent wins; prefer losing later
    if is_draw(board):
        return 0                # Draw

    available = get_available_moves(board)
    opponent = get_opponent(player)

    if player == maximizing_player:
        # Maximizing: AI's turn — pick highest valued move
        best_score = float('-inf')
        for move in available:
            new_board = make_move(board, move, player)
            score = minimax(new_board, opponent, maximizing_player, depth + 1)
            best_score = max(best_score, score)
        return best_score
    else:
        # Minimizing: Opponent's turn — pick lowest valued move
        best_score = float('inf')
        for move in available:
            new_board = make_move(board, move, player)
            score = minimax(new_board, opponent, maximizing_player, depth + 1)
            best_score = min(best_score, score)
        return best_score


def get_best_move(board: Board, player: str) -> Optional[int]:
    """
    Minimax strategy: find the move with the best minimax score.
    
    Args:
        board: Current board state
        player: AI player symbol ('X' or 'O')
    
    Returns:
        Optimal move index, or None if no moves available.
    """
    available = get_available_moves(board)
    if not available:
        return None

    opponent = get_opponent(player)
    best_score = float('-inf')
    best_move = available[0]

    for move in available:
        new_board = make_move(board, move, player)
        score = minimax(new_board, opponent, player, depth=1)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def get_move_explanation(board: Board, player: str) -> dict:
    """Returns move with minimax score details."""
    available = get_available_moves(board)
    opponent = get_opponent(player)
    move_scores = {}
    for move in available:
        new_board = make_move(board, move, player)
        move_scores[move] = minimax(new_board, opponent, player, depth=1)

    best_move = get_best_move(board, player)
    return {
        "move": best_move,
        "algorithm": "Minimax",
        "explanation": (
            f"Explored full game tree ({len(available)} initial branches). "
            f"Position {best_move} yields optimal outcome with score {move_scores.get(best_move, 0)}."
        ),
        "scores": move_scores
    }
