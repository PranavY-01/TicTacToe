/**
 * MoveHistory.jsx - Scrollable move history panel
 */

import React from "react";

export default function MoveHistory({ history }) {
    if (!history || history.length === 0) return null;

    const BOARD_MAP = [
        ["TL", "TC", "TR"],
        ["ML", "MC", "MR"],
        ["BL", "BC", "BR"],
    ];

    const positionLabel = (pos) => {
        const row = Math.floor(pos / 3);
        const col = pos % 3;
        return `${BOARD_MAP[row][col]} (${pos})`;
    };

    return (
        <div className="move-history">
            <h3 className="move-history__title">📋 Move History</h3>
            <div className="move-history__list">
                {history.map((move, i) => (
                    <div
                        key={i}
                        className={`move-history__item move-history__item--${move.type}`}
                    >
                        <span className="move-history__num">#{i + 1}</span>
                        <span
                            className={`move-history__player move-history__player--${move.player.toLowerCase()}`}
                        >
                            {move.player === "X" ? "✕" : "○"} {move.type === "ai" ? "AI" : "You"}
                        </span>
                        <span className="move-history__pos">{positionLabel(move.position)}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
