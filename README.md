# FP KKA Escape the cops
## 🚓 Escape The Police Maze Game 🍰

### 🎮 How to Play

1.  **Objective:** Escape the maze by reaching the exit (`vent.png`) after collecting all three cakes (`cake.png`).
2.  **Movement:** Use the **Arrow Keys** or **WASD** to move the player.
3.  **Winning:** Reach the exit once you have collected all the cakes (except in Endless Mode).
4.  **Losing:** Get caught by a police unit.

### 💡 Algorithmic Applications in the Game
#### 1\. Maze Generation (DFS Backtracker)

The maze structure is created using a recursive Depth-First Search (DFS) backtracker algorithm.

  * **Mechanism:** Starting from a point (1, 1), the algorithm randomly chooses a neighboring cell that hasn't been visited yet, carves a path through the wall separating them, and repeats the process recursively. If it reaches a dead end, it *backtracks* to the last cell with unvisited neighbors.
  * **Application Focus:** This method efficiently generates a **perfect maze**—a simply connected graph that ensures there is exactly one path between any two points (before loops are added).

#### 2\. Police Pathfinding (BFS vs. A\* Search)

The intelligence of the police units is determined by the pathfinding algorithm they use to locate and pursue the player.

| Game Mode | Algorithm Used | Complexity/Speed | Search Behavior |
| :--- | :--- | :--- | :--- |
| **Easy** | **Breadth-First Search (BFS)** | Guaranteed to find the shortest path, but **uninformed**. | Explores all possible paths layer-by-layer equally until the target is found, which can be computationally intensive in large areas.  |
| **Hard/Endless** | **A\* Search** | Guaranteed to find the shortest path, and is **informed** (generally faster). | Uses the **Manhattan Distance** heuristic to prioritize paths that move closer to the player, making the police movement targeted and efficient.  |
| **Exit Selection** | **Breadth-First Search (BFS)** | Used to measure the path distance. | Used to ensure the exit is chosen to maximize the shortest path distance from the starting point, creating a longer and more challenging maze. |

### 🛠️ Key Files and Algorithms

| File | Description | Core Algorithms/Concepts |
| :--- | :--- | :--- |
| `maze_generator.py` | Contains the `Maze` class and all the pathfinding functions. | **DFS Backtracker** (Maze Generation), **BFS** (Pathfinding), **A\* Search** (Informed Pathfinding), **Manhattan Heuristic**, **Adding Loops**. |
| `core.py` | Defines game objects like `Player`, `Police`, and `Coin`. | **Algorithm Selection Logic** (Police mode determines whether to use BFS or A\*). |
| `game.py` | Contains the main game loop, rendering, and game logic. | **Game State Management**, **Collision Detection**, **Enemy Spawning** (in Endless Mode). |
| `main.py` | Sets up the main menu and difficulty selection. | **Pygame Initialization**, **UI/Menu Logic**. |

### 🚀 Setup and Run

1.  **Prerequisites:** You need Python and Pygame installed.
    ```bash
    pip install pygame
    ```
2.  **Run:** Execute the `main.py` file to start the menu.
    ```bash
    python main.py
    ```
