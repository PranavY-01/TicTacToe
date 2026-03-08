"""
main.py - FastAPI Backend for Tic-Tac-Toe AI Platform

Endpoints:
  POST /start-game       - Initialize a new game
  POST /make-move        - Human player makes a move
  POST /ai-move          - Request AI move using selected algorithm
  GET  /game-state       - Get current game state
  GET  /algorithms       - List available AI algorithms
"""

import sys
import os

# Allow imports from the backend directory
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

from game_logic import (
    create_empty_board, make_move, is_valid_move,
    get_game_status, get_opponent, Board
)
import ai.random_agent as random_agent
import ai.greedy as greedy
import ai.minimax as minimax
import ai.alphabeta as alphabeta
import ai.astar_agent as astar_agent

# ─── App Setup ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Tic-Tac-Toe AI Platform",
    description="Play against AI agents using different decision-making algorithms.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── In-Memory Game Store ─────────────────────────────────────────────────────

games: dict[str, dict] = {}

# ─── Algorithm Registry ───────────────────────────────────────────────────────

ALGORITHMS = {
    "random": {
        "name": "Random",
        "module": random_agent,
        "description": "Selects a random legal move. Completely unpredictable. (Beginner)",
        "difficulty": "Very Easy"
    },
    "greedy": {
        "name": "Greedy",
        "module": greedy,
        "description": "Picks the move with the best immediate gain — wins if possible, blocks if needed. (Easy)",
        "difficulty": "Easy"
    },
    "minimax": {
        "name": "Minimax",
        "module": minimax,
        "description": "Explores the full game tree for optimal play. Never loses. (Hard)",
        "difficulty": "Hard"
    },
    "alphabeta": {
        "name": "Alpha-Beta Pruning",
        "module": alphabeta,
        "description": "Minimax with intelligent branch pruning — same optimal play, faster. (Hard)",
        "difficulty": "Hard"
    },
    "astar": {
        "name": "A* Search",
        "module": astar_agent,
        "description": "Best-first search using board evaluation heuristics. Prioritizes promising states. (Medium-Hard)",
        "difficulty": "Medium-Hard"
    }
}

# ─── Pydantic Models ──────────────────────────────────────────────────────────

class StartGameRequest(BaseModel):
    algorithm: str = "minimax"
    human_player: str = "X"   # 'X' or 'O'

class MakeMoveRequest(BaseModel):
    game_id: str
    position: int              # 0-8 index on the board

class AIMoveRequest(BaseModel):
    game_id: str

# ─── Helper Functions ─────────────────────────────────────────────────────────

def build_game_response(game: dict) -> dict:
    """Builds a standardized game state response."""
    status = get_game_status(game["board"])
    return {
        "game_id": game["game_id"],
        "board": game["board"],
        "current_player": game["current_player"],
        "human_player": game["human_player"],
        "ai_player": game["ai_player"],
        "algorithm": game["algorithm"],
        "algorithm_name": ALGORITHMS[game["algorithm"]]["name"],
        "status": status,
        "move_history": game["move_history"],
        "last_ai_explanation": game.get("last_ai_explanation"),
    }

# ─── API Endpoints ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Tic-Tac-Toe AI Platform API", "version": "1.0.0"}


@app.get("/algorithms")
def list_algorithms():
    """List all available AI algorithms."""
    return {
        "algorithms": [
            {
                "id": key,
                "name": val["name"],
                "description": val["description"],
                "difficulty": val["difficulty"]
            }
            for key, val in ALGORITHMS.items()
        ]
    }


@app.post("/start-game")
def start_game(req: StartGameRequest):
    """
    Initialize a new game session.
    Returns the game ID and initial state.
    """
    if req.algorithm not in ALGORITHMS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown algorithm '{req.algorithm}'. Choose from: {list(ALGORITHMS.keys())}"
        )
    if req.human_player not in ["X", "O"]:
        raise HTTPException(status_code=400, detail="human_player must be 'X' or 'O'")

    game_id = str(uuid.uuid4())
    ai_player = get_opponent(req.human_player)

    game = {
        "game_id": game_id,
        "board": create_empty_board(),
        "current_player": "X",          # X always starts
        "human_player": req.human_player,
        "ai_player": ai_player,
        "algorithm": req.algorithm,
        "move_history": [],
        "last_ai_explanation": None,
    }
    games[game_id] = game

    response = build_game_response(game)

    # If AI goes first (human is O), make AI move automatically
    if game["current_player"] == ai_player:
        ai_result = _execute_ai_move(game_id)
        return ai_result

    return response


@app.post("/make-move")
def make_human_move(req: MakeMoveRequest):
    """
    Human player makes a move at the given board position (0-8).
    Returns updated game state. If game continues, AI will also move.
    """
    if req.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game.")

    game = games[req.game_id]
    status = get_game_status(game["board"])

    if status["is_game_over"]:
        raise HTTPException(status_code=400, detail="Game is already over.")

    if game["current_player"] != game["human_player"]:
        raise HTTPException(status_code=400, detail="It's not your turn.")

    if not is_valid_move(game["board"], req.position):
        raise HTTPException(status_code=400, detail=f"Invalid move at position {req.position}.")

    # Apply human move
    game["board"] = make_move(game["board"], req.position, game["human_player"])
    game["move_history"].append({
        "player": game["human_player"],
        "position": req.position,
        "type": "human"
    })
    game["current_player"] = game["ai_player"]

    # Check if game ended after human move
    new_status = get_game_status(game["board"])
    if new_status["is_game_over"]:
        return build_game_response(game)

    # Execute AI move
    return _execute_ai_move(req.game_id)


@app.post("/ai-move")
def trigger_ai_move(req: AIMoveRequest):
    """
    Manually trigger the AI to make a move (for step-by-step control).
    Returns updated game state.
    """
    if req.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found.")

    game = games[req.game_id]
    status = get_game_status(game["board"])

    if status["is_game_over"]:
        raise HTTPException(status_code=400, detail="Game is already over.")

    if game["current_player"] != game["ai_player"]:
        raise HTTPException(status_code=400, detail="It's not the AI's turn.")

    return _execute_ai_move(req.game_id)


@app.get("/game-state/{game_id}")
def get_game_state(game_id: str):
    """Get current state of a specific game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found.")
    return build_game_response(games[game_id])


# ─── Internal AI Execution ────────────────────────────────────────────────────

def _execute_ai_move(game_id: str) -> dict:
    """Internal: execute the AI move for a game."""
    game = games[game_id]
    algo_key = game["algorithm"]
    algo_module = ALGORITHMS[algo_key]["module"]
    ai_player = game["ai_player"]

    # Get explanation (which also computes the move)
    result = algo_module.get_move_explanation(game["board"], ai_player)
    ai_move = result["move"]

    if ai_move is None:
        return build_game_response(game)

    # Apply AI move
    game["board"] = make_move(game["board"], ai_move, ai_player)
    game["move_history"].append({
        "player": ai_player,
        "position": ai_move,
        "type": "ai",
        "algorithm": result["algorithm"],
        "explanation": result["explanation"]
    })
    game["last_ai_explanation"] = result
    game["current_player"] = game["human_player"]

    return build_game_response(game)
