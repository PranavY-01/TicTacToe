# Tic-Tac-Toe AI — Algorithm Showdown

A full-stack Tic-Tac-Toe platform where you play against AI agents powered by **5 different decision-making algorithms**. Built with **React + Vite** (frontend) and **FastAPI + Python** (backend).

---

## ✨ Algorithms Implemented

| Algorithm | Difficulty | Strategy |
|---|---|---|
| 🎲 **Random** | Very Easy | Picks any legal move randomly — purely unpredictable |
| 🤑 **Greedy** | Easy | Wins if it can, blocks if needed, prefers center/corners |
| 🧠 **Minimax** | Hard | Explores the full game tree — never makes a suboptimal move |
| ⚡ **Alpha-Beta Pruning** | Hard | Same as Minimax but prunes irrelevant branches faster |
| 🌟 **A\* Search** | Medium-Hard | Best-first heuristic search using board state evaluation |

---

## 🚀 Quick Start

### 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at: **http://localhost:5173**

---

## 📁 Project Structure

```
tic-tac-toe-ai/
├── backend/
│   ├── main.py              # FastAPI app, all endpoints
│   ├── game_logic.py        # Core game logic (win/draw detection, validation)
│   ├── requirements.txt
│   └── ai/
│       ├── __init__.py
│       ├── random_agent.py  # Random strategy
│       ├── greedy.py        # Greedy algorithm
│       ├── minimax.py       # Minimax (full game tree)
│       ├── alphabeta.py     # Minimax + Alpha-Beta pruning
│       └── astar_agent.py   # A* search with heuristic evaluation
│
└── frontend/
    ├── index.html
    ├── package.json
    └── src/
        ├── App.jsx           # Root component, game state management
        ├── api.js            # REST API client
        ├── index.css         # Full design system (dark/neon theme)
        └── components/
            ├── Board.jsx     # 3×3 grid
            ├── Cell.jsx      # Individual cell (with animations)
            ├── Controls.jsx  # Algorithm selector, status, AI explanation
            └── MoveHistory.jsx  # Scrollable history panel
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/algorithms` | List all AI algorithms |
| `POST` | `/start-game` | Initialize a new game session |
| `POST` | `/make-move` | Human player makes a move |
| `POST` | `/ai-move` | Trigger AI move manually |
| `GET` | `/game-state/{id}` | Get full game state |
| `GET` | `/docs` | Interactive Swagger UI |

### Example: Start a Game

```bash
curl -X POST http://localhost:8000/start-game \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "minimax", "human_player": "X"}'
```

### Example: Make a Move

```bash
curl -X POST http://localhost:8000/make-move \
  -H "Content-Type: application/json" \
  -d '{"game_id": "<your-game-id>", "position": 4}'
```

---

## 🧠 Algorithm Deep Dive

### Random
Calls `random.choice(available_moves)`. Zero intelligence — serves as a baseline to prove smarter algorithms outperform it.

### Greedy
Scores each available move by immediate benefit only:
- **+100** if this move wins the game
- **+10** if this move blocks opponent's win  
- **+5/3/1** for center/corner/edge positions  

No lookahead — can be tricked with 2-move setups (forks).

### Minimax
Recursively evaluates every possible future game state. Returns the optimal move assuming both players play perfectly. The AI is **unbeatable** — at best you draw.

Score function:  
- `+10 - depth` for AI win (rewards winning sooner)  
- `depth - 10` for opponent win (delays losing)  
- `0` for draw

### Alpha-Beta Pruning
Identical outcome to Minimax but maintains two bounds:
- **α (alpha)**: best guaranteed score for the maximizer
- **β (beta)**: best guaranteed score for the minimizer  

When `β ≤ α`, the branch is pruned — the opponent would never let this path happen. Significantly reduces nodes evaluated.

### A\* Search
Uses a min-heap priority queue. Each board state is scored by:
- `g(n)` = depth (moves made)  
- `h(n)` = heuristic evaluating lines, threats, center/corner control  
- `f(n) = -h(n) + g(n)` — expands most promising states first

Heuristic awards:
- **+10** for 2-in-a-row with open third (near win)
- **-10** for opponent 2-in-a-row (near loss / must block)
- **+/-2** for center, **+/-1** for corners

---

## 🎮 How to Play

1. Select an AI algorithm from the dropdown
2. Choose whether you play as X (goes first) or O (goes second)
3. Click **▶ Start Game**
4. Click cells on the board to place your symbol
5. Watch the **AI Reasoning** panel to see how the algorithm decided
6. View **Move History** on the right sidebar
7. Click **🔄 Restart Game** to try a different algorithm

---

## ⚙️ Tech Stack

- **Frontend**: React 18, Vite 7, Vanilla CSS (glassmorphism + dark theme)
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn
- **Communication**: REST API (JSON)
- **Fonts**: Inter + Space Grotesk (Google Fonts)

---

## 👨‍💻 Developer

- **Name:** Pranav
- **GitHub:** PranavY-01
- **Email:** pranavmusicals9@gmail.com
