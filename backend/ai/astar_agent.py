"""
astar_agent.py - A* Search adapted for Tic-Tac-Toe

A* is a best-first search algorithm that uses a heuristic to estimate
the "cost" from current state to the goal.

Adaptation for Tic-Tac-Toe:
  - "Goal" = winning board state
  - g(n) = depth (number of moves made)
  - h(n) = heuristic score based on board analysis
  - f(n) = -h(n) + g(n) (we expand most promising states first)

The heuristic evaluates:
  - How many lines the AI controls exclusively
  - How many lines are blocked by the opponent
  - Threat detection (2-in-a-row with open third)

Behavior: Heuristic-driven, strong but not always perfect.
          Prioritizes moves that look promising via evaluation function.
Difficulty: Medium-Hard
"""

import heapq
from typing import Optional
from game_logic import (
    Board, get_available_moves, make_move, check_winner,
    is_draw, is_game_over, get_opponent
)

WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],   # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],   # columns
    [0, 4, 8], [2, 4, 6],               # diagonals
]


def heuristic(board: Board, player: str) -> float:
    """
    A* heuristic: estimates desirability of a board state for `player`.
    
    Scoring:
      +1000 = AI (player) wins
      -1000 = Opponent wins
      +10   per line with 2 AI pieces and 1 empty (potential win)
      +3    per line with 1 AI piece and 2 empty
      -10   per line with 2 opponent pieces and 1 empty (blocking needed)
      -3    per line with 1 opponent piece and 2 empty
      +2    for controlling center
      +1    for controlling corners
    """
    opponent = get_opponent(player)
    score = 0.0

    winner = check_winner(board)
    if winner == player:
        return 1000.0
    if winner == opponent:
        return -1000.0

    for combo in WIN_COMBINATIONS:
        line = [board[i] for i in combo]
        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(None)

        if opponent_count == 0:
            # Line reachable for AI
            if player_count == 2 and empty_count == 1:
                score += 10     # near win
            elif player_count == 1 and empty_count == 2:
                score += 3

        if player_count == 0:
            # Line reachable for opponent
            if opponent_count == 2 and empty_count == 1:
                score -= 10     # near loss, must block
            elif opponent_count == 1 and empty_count == 2:
                score -= 3

    # Positional bonuses
    if board[4] == player:
        score += 2      # center
    elif board[4] == opponent:
        score -= 2

    for corner in [0, 2, 6, 8]:
        if board[corner] == player:
            score += 1
        elif board[corner] == opponent:
            score -= 1

    return score


def get_best_move(board: Board, player: str) -> Optional[int]:
    """
    A* Search strategy.
    
    Uses a priority queue (min-heap) to expand the highest-scoring moves first.
    Each state in the heap: (f_cost, g_cost, move_sequence, board_state)
    
    We search up to a limited depth to find the best first move
    using A*-style best-first ordering.
    
    Args:
        board: Current board state
        player: AI player symbol
    
    Returns:
        Best first move index found by A* heuristic search.
    """
    available = get_available_moves(board)
    if not available:
        return None

    # Priority queue: (negative_f, depth, first_move, current_board, current_player)
    # We store negative f because heapq is a min-heap
    heap = []
    opponent = get_opponent(player)

    # Seed the heap with initial moves
    for move in available:
        new_board = make_move(board, move, player)
        g = 1
        h = heuristic(new_board, player)
        f = -h + g  # lower f = higher priority
        # Tiebreak: use move index for determinism
        heapq.heappush(heap, (f, g, move, move, new_board, opponent))

    best_move = available[0]
    best_score = float('-inf')

    # Track explored states to avoid revisiting
    explored = set()

    while heap:
        f, g, first_move, _, current_board, current_player = heapq.heappop(heap)

        board_key = (tuple(current_board), current_player)
        if board_key in explored:
            continue
        explored.add(board_key)

        h = heuristic(current_board, player)

        # For root-level move selection, track best first move
        if g == 1 and (-h + g) < (-best_score + 1):
            if h > best_score:
                best_score = h
                best_move = first_move

        # Expand further if game isn't over and depth < 6
        if not is_game_over(current_board) and g < 6:
            next_moves = get_available_moves(current_board)
            for next_move in next_moves:
                next_board = make_move(current_board, next_move, current_player)
                next_opponent = get_opponent(current_player)
                new_g = g + 1
                new_h = heuristic(next_board, player)
                new_f = -new_h + new_g
                heapq.heappush(heap, (new_f, new_g, first_move, next_move, next_board, next_opponent))

    # Fallback: evaluate all root moves directly using heuristic
    if not available:
        return None

    final_best = available[0]
    final_best_score = float('-inf')
    for move in available:
        nb = make_move(board, move, player)
        s = heuristic(nb, player)
        if s > final_best_score:
            final_best_score = s
            final_best = move

    # If A* found a better move, use it, otherwise fallback to direct heuristic
    astar_board = make_move(board, best_move, player)
    astar_score = heuristic(astar_board, player)
    direct_board = make_move(board, final_best, player)
    direct_score = heuristic(direct_board, player)

    return best_move if astar_score >= direct_score else final_best


def get_move_explanation(board: Board, player: str) -> dict:
    """Returns move with A* heuristic scores."""
    available = get_available_moves(board)
    move_scores = {}
    for move in available:
        nb = make_move(board, move, player)
        move_scores[move] = round(heuristic(nb, player), 2)

    best_move = get_best_move(board, player)
    return {
        "move": best_move,
        "algorithm": "A* Search",
        "explanation": (
            f"Used A* best-first search with heuristic evaluation. "
            f"Position {best_move} has heuristic score {move_scores.get(best_move, 0)} "
            f"(higher = better for AI)."
        ),
        "scores": move_scores
    }
