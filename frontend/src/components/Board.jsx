/**
 * Board.jsx - 3x3 Tic-Tac-Toe grid
 */

import React from "react";
import Cell from "./Cell";

export default function Board({
    board,
    winningLine,
    onCellClick,
    disabled,
    lastMoveIndex,
}) {
    return (
        <div className="board" role="grid" aria-label="Tic-Tac-Toe Board">
            {board.map((cell, index) => (
                <Cell
                    key={index}
                    index={index}
                    value={cell}
                    onClick={onCellClick}
                    isWinning={winningLine?.includes(index)}
                    isDisabled={disabled}
                    lastMove={index === lastMoveIndex}
                />
            ))}
        </div>
    );
}
