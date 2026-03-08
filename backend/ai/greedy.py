"""
greedy.py - Greedy Algorithm AI
Evaluates immediate board advantages without lookahead.

Strategy:
  1. Win immediately if possible (offense)
  2. Block opponent's immediate win (defense)
  3. Prefer center, then corners, then edges

Behavior: Makes the locally optimal move without planning ahead.
Difficulty: Easy-Medium
"""

from typing import Optional
from game_logic import Board, get_available_moves, make_move, check_winner, get_opponent


# Position priority: center > corners > edges
POSITION_PRIORITY = [4, 0, 2, 6, 8, 1, 3, 5, 7]


def score_move(board: Board, index: int, player: str) -> int:
    """
    Scores a single move based on immediate benefit.
    Higher score = better move.
    
    Scoring:
      +100 if this move wins the game
       +10 if this move blocks opponent from winning
        +5 if occupying center
        +3 if occupying a corner
        +1 if occupying an edge
    """
    score = 0
    new_board = make_move(board, index, player)
    opponent = get_opponent(player)

    # Check if this move wins the game
    if check_winner(new_board) == player:
        score += 100
        return score

    # Check if blocking opponent from winning
    block_board = make_move(board, index, opponent)
    if check_winner(block_board) == opponent:
        score += 10

    # Positional scoring
    if index == 4:
        score += 5        # center
    elif index in [0, 2, 6, 8]:
        score += 3        # corners
    else:
        score += 1        # edges

    return score


def get_best_move(board: Board, player: str) -> Optional[int]:
    """
    Greedy strategy: choose the move with highest immediate score.
    
    Args:
        board: Current board state
        player: AI player symbol ('X' or 'O')
    
    Returns:
        Best immediate move index, or None if no moves available.
    """
    available = get_available_moves(board)
    if not available:
        return None

    best_score = -1
    best_move = available[0]

    for move in available:
        score = score_move(board, move, player)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def get_move_explanation(board: Board, player: str) -> dict:
    """Returns move with score breakdown for explanation."""
    available = get_available_moves(board)
    move_scores = {m: score_move(board, m, player) for m in available}
    best_move = get_best_move(board, player)
    return {
        "move": best_move,
        "algorithm": "Greedy",
        "explanation": (
            f"Evaluated {len(available)} moves by immediate gain. "
            f"Selected position {best_move} with score {move_scores.get(best_move, 0)}."
        ),
        "scores": move_scores
    }
