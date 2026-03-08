/**
 * api.js - Frontend API client for Tic-Tac-Toe backend
 * All REST calls to the FastAPI backend go through here.
 */

const BASE_URL = "http://localhost:8000";

/**
 * Generic fetch wrapper with error handling.
 */
async function apiFetch(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Fetch list of available AI algorithms.
 * @returns {Promise<{algorithms: Array}>}
 */
export async function fetchAlgorithms() {
  return apiFetch("/algorithms");
}

/**
 * Start a new game session.
 * @param {string} algorithm - Algorithm ID (e.g. 'minimax')
 * @param {string} humanPlayer - 'X' or 'O'
 * @returns {Promise<GameState>}
 */
export async function startGame(algorithm, humanPlayer = "X") {
  return apiFetch("/start-game", {
    method: "POST",
    body: JSON.stringify({ algorithm, human_player: humanPlayer }),
  });
}

/**
 * Make a move as the human player.
 * @param {string} gameId - Current game ID
 * @param {number} position - Board index (0-8)
 * @returns {Promise<GameState>}
 */
export async function makeMove(gameId, position) {
  return apiFetch("/make-move", {
    method: "POST",
    body: JSON.stringify({ game_id: gameId, position }),
  });
}

/**
 * Trigger the AI to make a move.
 * @param {string} gameId - Current game ID
 * @returns {Promise<GameState>}
 */
export async function triggerAiMove(gameId) {
  return apiFetch("/ai-move", {
    method: "POST",
    body: JSON.stringify({ game_id: gameId }),
  });
}

/**
 * Fetch current game state.
 * @param {string} gameId
 * @returns {Promise<GameState>}
 */
export async function getGameState(gameId) {
  return apiFetch(`/game-state/${gameId}`);
}
