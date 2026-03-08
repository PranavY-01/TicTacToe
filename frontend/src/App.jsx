/**
 * App.jsx - Root application component
 * Manages global state, API calls, and layout orchestration.
 */

import React, { useState, useEffect, useCallback } from "react";
import Board from "./components/Board";
import Controls from "./components/Controls";
import MoveHistory from "./components/MoveHistory";
import { fetchAlgorithms, startGame, makeMove } from "./api";

export default function App() {
  // ─── State ────────────────────────────────────────────────────────────────
  const [algorithms, setAlgorithms] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("minimax");
  const [humanPlayer, setHumanPlayer] = useState("X");
  const [gameState, setGameState] = useState(null);
  const [gameActive, setGameActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastMoveIndex, setLastMoveIndex] = useState(null);
  const [aiThinking, setAiThinking] = useState(false);

  // ─── Load algorithms on mount ─────────────────────────────────────────────
  useEffect(() => {
    fetchAlgorithms()
      .then((data) => setAlgorithms(data.algorithms))
      .catch(() => setError("Could not connect to backend. Is the server running?"));
  }, []);

  // ─── Start a new game ─────────────────────────────────────────────────────
  const handleStart = useCallback(async () => {
    setLoading(true);
    setError(null);
    setLastMoveIndex(null);
    try {
      const state = await startGame(selectedAlgorithm, humanPlayer);
      setGameState(state);
      setGameActive(true);

      // If AI moved first (we are O), mark its position
      if (state.move_history && state.move_history.length > 0) {
        setLastMoveIndex(state.move_history[state.move_history.length - 1].position);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [selectedAlgorithm, humanPlayer]);

  // ─── Handle cell click ────────────────────────────────────────────────────
  const handleCellClick = useCallback(
    async (index) => {
      if (!gameActive || !gameState) return;
      if (gameState.status.is_game_over) return;
      if (gameState.current_player !== gameState.human_player) return;
      if (gameState.board[index] !== null) return;

      setLoading(true);
      setError(null);
      setAiThinking(false);

      try {
        setLastMoveIndex(index);
        const updatedState = await makeMove(gameState.game_id, index);
        setGameState(updatedState);

        // Mark AI's move
        if (updatedState.move_history && updatedState.move_history.length > 0) {
          const lastMove = updatedState.move_history[updatedState.move_history.length - 1];
          if (lastMove.type === "ai") {
            setLastMoveIndex(lastMove.position);
          }
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
        setAiThinking(false);
      }
    },
    [gameActive, gameState]
  );

  // ─── Restart ──────────────────────────────────────────────────────────────
  const handleRestart = useCallback(() => {
    setGameState(null);
    setGameActive(false);
    setError(null);
    setLastMoveIndex(null);
    setAiThinking(false);
  }, []);

  // ─── Board state ──────────────────────────────────────────────────────────
  const board = gameState?.board ?? Array(9).fill(null);
  const winningLine = gameState?.status?.winning_line ?? null;
  const isBoardDisabled =
    loading ||
    aiThinking ||
    !gameActive ||
    gameState?.status?.is_game_over ||
    gameState?.current_player !== gameState?.human_player;

  const isGameOver = gameState?.status?.is_game_over;

  return (
    <div className="app">
      {/* Background particles */}
      <div className="bg-particles" aria-hidden="true">
        {Array.from({ length: 20 }).map((_, i) => (
          <div key={i} className="particle" style={{ "--i": i }} />
        ))}
      </div>

      {/* Layout */}
      <div className="layout">
        {/* Left - Controls */}
        <Controls
          algorithms={algorithms}
          selectedAlgorithm={selectedAlgorithm}
          onAlgorithmChange={setSelectedAlgorithm}
          humanPlayer={humanPlayer}
          onHumanPlayerChange={setHumanPlayer}
          onStart={handleStart}
          onRestart={handleRestart}
          gameActive={gameActive}
          loading={loading}
          gameState={gameState}
          error={error}
        />

        {/* Center - Board */}
        <main className="game-area">
          <div className="game-area__inner">
            {/* Game over overlay text */}
            {isGameOver && (
              <div className={`result-banner result-banner--${gameState.status.winner === gameState.human_player
                  ? "win"
                  : gameState.status.is_draw
                    ? "draw"
                    : "lose"
                }`}>
                {gameState.status.winner === gameState.human_player
                  ? "🎉 You Win!"
                  : gameState.status.is_draw
                    ? "🤝 Draw!"
                    : "🤖 AI Wins!"}
              </div>
            )}

            {/* Board */}
            <div className={`board-wrapper ${isGameOver ? "board-wrapper--over" : ""} ${aiThinking ? "board-wrapper--thinking" : ""}`}>
              <Board
                board={board}
                winningLine={winningLine}
                onCellClick={handleCellClick}
                disabled={isBoardDisabled}
                lastMoveIndex={lastMoveIndex}
              />
            </div>

            {/* AI thinking indicator */}
            {(loading || aiThinking) && gameActive && !isGameOver && (
              <div className="thinking-indicator">
                <span className="thinking-dot" />
                <span className="thinking-dot" />
                <span className="thinking-dot" />
                <span className="thinking-label">
                  {gameState?.current_player === gameState?.ai_player
                    ? `${gameState?.algorithm_name} thinking...`
                    : "Processing..."}
                </span>
              </div>
            )}

            {/* Start prompt */}
            {!gameActive && !loading && (
              <div className="start-prompt">
                <p>Select an algorithm and start a game!</p>
              </div>
            )}
          </div>
        </main>

        {/* Right - Move History */}
        <aside className="history-panel">
          <MoveHistory history={gameState?.move_history ?? []} />
        </aside>
      </div>
    </div>
  );
}
