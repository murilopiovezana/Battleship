# 🛳️ Battleship Player

A Python-based AI agent that plays the classic game of Battleship. This project was developed as an assignment for the MC102 (Algorithms and Data Structures) course.

The core of the project is the `player_aluno.py` file, which contains a custom-designed AI strategy for both placing ships and attacking the opponent. The AI competes against pre-defined bots (linear and random) within a game engine that supports a Pygame-based GUI and a command-line tournament mode for statistical analysis.

## 🎯 My Strategy

The goal was to create an efficient AI that could consistently win against the provided bots. My implementation is divided into two key parts:

### 1. Ship Placement (`posicoes_navios`)
The ships are placed in a fixed, strategic pattern. The larger ships ("Carrier" and "Battleship") are positioned along the top edge, while the smaller ships are placed along the bottom edge. This spreads the fleet across the board, making it harder for simple linear-scanning opponents to find all ships quickly. This was made in order to make sure that the linear bot, in a 10x10 board, always needs to make 100 guesses to win the game. Obviously, it is not the best positioning strategy overall, but it works in our favor in this assignment.

### 2. Attack Logic (`jogar`)
The attack strategy follows a "Hunter-Killer" model, which operates in three phases:

1.  **Initial Hunt:** The first four moves are always to the four corners of the board (`(0,0)`, `(0,9)`, `(9,0)`, `(9,9)`). This is a high-probability way to find at least one ship early, since the linear bot always positions at least one ship over one edge of the board.
2.  **Target Mode (Killer):** Once a part of a ship is hit (`NAVIO_ENCONTRADO`), the algorithm switches to "Target Mode." It systematically attacks all adjacent (up, down, left, right) unknown cells around the hit to quickly find the rest of the ship and sink it.
3.  **Random Hunt:** If there are no known hits to target, the AI reverts to "Hunt Mode," making random attacks on unknown cells until a new ship is found, at which point it switches back to Target Mode.

This combination ensures a methodical approach to clearing the board, prioritizing confirmed targets before searching for new ones.

## 🚀 How to Run

### Prerequisites
Ensure you have Python installed. Then, install the required libraries:
```bash
pip install pygame tqdm
```

### Running the Game
You can run a single game against a bot from your terminal.

**With Graphical Interface (GUI):**
```bash
# Play against the Linear Bot
python game.py -l

# Play against the Random Bot
python game.py -r
```

**Without Graphical Interface (Terminal Only):**
```bash
# Play against the Linear Bot (no GUI)
python game.py -l --no-gui

# Play against the Random Bot (no GUI)
python game.py -r --no-gui
```

### Running the Tournament
To evaluate the AI's performance over many games, run the tournament script. It will play 1000 games against each bot and save the results to `resultado_torneio.txt`.
```bash
python tournament.py
```

## 📂 Project Structure
```
.
├── player_aluno.py      # <-- My AI implementation
├── game.py              # Main script to run the game
├── engine.py            # Core game logic and turn management
├── tournament.py        # Runs bulk simulations for performance analysis
├── gui.py               # Pygame-based graphical user interface
├── constants.py         # Game constants (board size, ship info)
├── classes/             # Directory for game object classes
│   ├── bot_linear.py    # AI for the Linear Bot
│   ├── bot_random.py    # AI for the Random Bot
│   ├── _board.py        # Tabuleiro (Board) class
│   ├── _ship.py         # Navio (Ship) class
│   └── ...              # Other helper classes
└── ASSIGNMENT_PT.md     # The original university assignment brief (in Portuguese)
```
