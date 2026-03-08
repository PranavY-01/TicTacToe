/**
 * Controls.jsx - Game controls panel
 * Includes: algorithm selector, player selector, start/restart button,
 *           status display, and AI explanation panel.
 */

import React from "react";

const DIFFICULTY_COLORS = {
    "Very Easy": "#4ade80",
    Easy: "#a3e635",
    "Medium-Hard": "#fbbf24",
    Hard: "#f87171",
};

export default function Controls({
    algorithms,
    selectedAlgorithm,
    onAlgorithmChange,
    humanPlayer,
    onHumanPlayerChange,
    onStart,
    onRestart,
    gameActive,
    loading,
    gameState,
    error,
}) {
    const currentAlgo = algorithms.find((a) => a.id === selectedAlgorithm);
    const explanation = gameState?.last_ai_explanation;

    const getStatusMessage = () => {
        if (!gameState) return null;
        const status = gameState.status;
        if (status.winner) {
            if (status.winner === gameState.human_player) return { text: "🎉 You win!", type: "win" };
            return { text: "🤖 AI wins!", type: "lose" };
        }
        if (status.is_draw) return { text: "🤝 It's a draw!", type: "draw" };
        if (gameState.current_player === gameState.human_player)
            return { text: "Your turn", type: "your-turn" };
        return { text: "AI is thinking...", type: "ai-turn" };
    };

    const statusMsg = getStatusMessage();

    return (
        <aside className="controls">
            {/* Header */}
            <div className="controls__header">
                <div className="controls__logo">🎮</div>
                <h1 className="controls__title">Tic-Tac-Toe AI</h1>
                <p className="controls__subtitle">Algorithm Showdown</p>
            </div>

            <div className="controls__divider" />

            {/* Algorithm Selector */}
            <div className="controls__section">
                <label className="controls__label" htmlFor="algo-select">
                    🧠 AI Algorithm
                </label>
                <div className="controls__select-wrapper">
                    <select
                        id="algo-select"
                        className="controls__select"
                        value={selectedAlgorithm}
                        onChange={(e) => onAlgorithmChange(e.target.value)}
                        disabled={gameActive && !gameState?.status?.is_game_over}
                    >
                        {algorithms.map((algo) => (
                            <option key={algo.id} value={algo.id}>
                                {algo.name} — {algo.difficulty}
                            </option>
                        ))}
                    </select>
                </div>

                {currentAlgo && (
                    <div className="controls__algo-info">
                        <span
                            className="controls__difficulty-badge"
                            style={{ background: DIFFICULTY_COLORS[currentAlgo.difficulty] + "22", color: DIFFICULTY_COLORS[currentAlgo.difficulty] }}
                        >
                            {currentAlgo.difficulty}
                        </span>
                        <p className="controls__algo-desc">{currentAlgo.description}</p>
                    </div>
                )}
            </div>

            {/* Player Selector */}
            <div className="controls__section">
                <label className="controls__label">⚔️ Play as</label>
                <div className="controls__player-toggle">
                    <button
                        className={`controls__player-btn ${humanPlayer === "X" ? "active" : ""}`}
                        onClick={() => onHumanPlayerChange("X")}
                        disabled={gameActive && !gameState?.status?.is_game_over}
                    >
                        ✕ X (goes first)
                    </button>
                    <button
                        className={`controls__player-btn ${humanPlayer === "O" ? "active" : ""}`}
                        onClick={() => onHumanPlayerChange("O")}
                        disabled={gameActive && !gameState?.status?.is_game_over}
                    >
                        ○ O (goes second)
                    </button>
                </div>
            </div>

            <div className="controls__divider" />

            {/* Action Buttons */}
            <div className="controls__section">
                {!gameActive ? (
                    <button
                        className="controls__btn controls__btn--primary"
                        onClick={onStart}
                        disabled={loading}
                    >
                        {loading ? "Starting..." : "▶ Start Game"}
                    </button>
                ) : (
                    <button
                        className="controls__btn controls__btn--danger"
                        onClick={onRestart}
                        disabled={loading}
                    >
                        🔄 Restart Game
                    </button>
                )}
            </div>

            {/* Error */}
            {error && (
                <div className="controls__error">
                    ⚠️ {error}
                </div>
            )}

            {/* Game Status */}
            {statusMsg && gameActive && (
                <div className={`controls__status controls__status--${statusMsg.type}`}>
                    <span className="controls__status-text">{statusMsg.text}</span>
                </div>
            )}

            {/* Game Info */}
            {gameState && gameActive && (
                <div className="controls__section">
                    <div className="controls__info-grid">
                        <div className="controls__info-item">
                            <span className="controls__info-label">You</span>
                            <span className="controls__info-value">{gameState.human_player}</span>
                        </div>
                        <div className="controls__info-item">
                            <span className="controls__info-label">AI</span>
                            <span className="controls__info-value">{gameState.ai_player}</span>
                        </div>
                        <div className="controls__info-item">
                            <span className="controls__info-label">Moves</span>
                            <span className="controls__info-value">{gameState.status.move_count}</span>
                        </div>
                        <div className="controls__info-item">
                            <span className="controls__info-label">Algo</span>
                            <span className="controls__info-value" style={{ fontSize: "0.65rem" }}>
                                {gameState.algorithm_name}
                            </span>
                        </div>
                    </div>
                </div>
            )}

            {/* AI Explanation */}
            {explanation && gameActive && (
                <div className="controls__explanation">
                    <div className="controls__explanation-header">
                        <span className="controls__explanation-icon">💡</span>
                        <span className="controls__explanation-title">AI Reasoning</span>
                    </div>
                    <p className="controls__explanation-text">{explanation.explanation}</p>
                    {explanation.scores && Object.keys(explanation.scores).length > 0 && (
                        <div className="controls__scores">
                            <span className="controls__scores-label">Move scores:</span>
                            <div className="controls__scores-grid">
                                {Object.entries(explanation.scores)
                                    .sort(([, a], [, b]) => b - a)
                                    .slice(0, 5)
                                    .map(([pos, score]) => (
                                        <div key={pos} className="controls__score-item">
                                            <span>Pos {pos}</span>
                                            <span style={{ color: score > 0 ? "#4ade80" : score < 0 ? "#f87171" : "#94a3b8" }}>
                                                {score}
                                            </span>
                                        </div>
                                    ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </aside>
    );
}
