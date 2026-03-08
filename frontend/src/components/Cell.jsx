/**
 * Cell.jsx - Single Tic-Tac-Toe board cell
 */

import React from "react";

export default function Cell({ value, index, onClick, isWinning, isDisabled, lastMove }) {
    const symbol = value === "X" ? "✕" : value === "O" ? "○" : null;

    return (
        <button
            className={[
                "cell",
                value ? `cell--${value.toLowerCase()}` : "",
                isWinning ? "cell--winning" : "",
                lastMove ? "cell--last-move" : "",
                isDisabled || value ? "cell--disabled" : "cell--playable",
            ]
                .filter(Boolean)
                .join(" ")}
            onClick={() => !isDisabled && !value && onClick(index)}
            aria-label={`Cell ${index + 1}${value ? `, ${value}` : ", empty"}`}
            disabled={isDisabled || !!value}
        >
            {symbol && (
                <span className="cell-symbol" key={value}>
                    {symbol}
                </span>
            )}
        </button>
    );
}
