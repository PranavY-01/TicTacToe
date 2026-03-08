"""
random_agent.py - Random Strategy AI
Selects any available legal move at random.
This serves as the baseline/easiest opponent.

Behavior: Completely unpredictable, makes no strategic decisions.
Difficulty: Very Easy
"""

import random
from typing import Optional
from game_logic import Board, get_available_moves


def get_best_move(board: Board, player: str) -> Optional[int]:
    """
    Random strategy: pick any available move randomly.
    
    Args:
        board: Current board state (list of 9: 'X', 'O', or None)
        player: The AI's player symbol ('X' or 'O')
    
    Returns:
        A random valid move index, or None if no moves available.
    """
    available = get_available_moves(board)
    if not available:
        return None
    return random.choice(available)


def get_move_explanation(board: Board, player: str) -> dict:
    """Returns the move and an explanation of the decision."""
    move = get_best_move(board, player)
    return {
        "move": move,
        "algorithm": "Random",
        "explanation": f"Randomly selected position {move} from {len(get_available_moves(board))} available positions."
    }
