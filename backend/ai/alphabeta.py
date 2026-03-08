"""
alphabeta.py - Minimax with Alpha-Beta Pruning AI
Optimized adversarial search that prunes unnecessary branches.

Strategy:
  Same as Minimax but tracks alpha (best for maximizer) and
  beta (best for minimizer) to skip branches that can't affect outcome.
  Produces IDENTICAL results to Minimax but much faster.

Behavior: Same optimal play as Minimax; faster computation.
Difficulty: Hard (optimal play, same as Minimax)
"""

from typing import Optional
from game_logic import (
    Board, get_available_moves, make_move, check_winner,
    is_draw, get_opponent
)


def alphabeta(
    board: Board,
    player: str,
    maximizing_player: str,
    alpha: float,
    beta: float,
    depth: int = 0
) -> int:
    """
    Minimax with Alpha-Beta pruning.
    
    Args:
        board: Current board state
        player: Whose turn it is
        maximizing_player: The AI's symbol
        alpha: Best score guaranteed for maximizer so far
        beta: Best score guaranteed for minimizer so far
        depth: Current recursion depth
    
    Pruning logic:
        - If beta <= alpha, the current branch is irrelevant
          (maximizer will never pick this path, or vice versa).
    
    Returns:
        Optimal score from AI's perspective.
    """
    winner = check_winner(board)
    if winner == maximizing_player:
        return 10 - depth
    if winner is not None:
        return depth - 10
    if is_draw(board):
        return 0

    available = get_available_moves(board)
    opponent = get_opponent(player)

    if player == maximizing_player:
        best_score = float('-inf')
        for move in available:
            new_board = make_move(board, move, player)
            score = alphabeta(new_board, opponent, maximizing_player, alpha, beta, depth + 1)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break   # Beta cut-off: minimizer won't allow this branch
        return best_score
    else:
        best_score = float('inf')
        for move in available:
            new_board = make_move(board, move, player)
            score = alphabeta(new_board, opponent, maximizing_player, alpha, beta, depth + 1)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break   # Alpha cut-off: maximizer won't allow this branch
        return best_score


def get_best_move(board: Board, player: str) -> Optional[int]:
    """
    Alpha-Beta Pruning strategy: find optimal move, faster than pure Minimax.
    
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
    alpha = float('-inf')
    beta = float('inf')

    for move in available:
        new_board = make_move(board, move, player)
        score = alphabeta(new_board, opponent, player, alpha, beta, depth=1)
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)

    return best_move


def get_move_explanation(board: Board, player: str) -> dict:
    """Returns move with alpha-beta score details."""
    available = get_available_moves(board)
    opponent = get_opponent(player)
    move_scores = {}
    for move in available:
        new_board = make_move(board, move, player)
        move_scores[move] = alphabeta(
            new_board, opponent, player,
            float('-inf'), float('inf'), depth=1
        )

    best_move = get_best_move(board, player)
    return {
        "move": best_move,
        "algorithm": "Alpha-Beta Pruning",
        "explanation": (
            f"Explored game tree with pruning — skipped branches where alpha >= beta. "
            f"Position {best_move} is optimal with score {move_scores.get(best_move, 0)}."
        ),
        "scores": move_scores
    }
