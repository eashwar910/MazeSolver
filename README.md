# Maze Solver

This is a simple **Maze Generator and Solver** application built using **Pygame**.

## Overview

This application generates a maze using **Kruskal's Algorithm** and represents it visually using **Pygame**. The generated maze consists of a **71x71** 2D list where:
- `1s` represent walls
- `0s` represent open paths

Once generated, the maze can be solved using various search algorithms.

## Features
- **Maze Generation** using **Kruskal's Algorithm**
- **Maze Solving** using:
  - Breadth-First Search (**BFS**)
  - Depth-First Search (**DFS**)
  - A* Search (**A-Star Algorithm**)
  - Greedy Best-First Search
- **Visual Representation** using **Pygame**

## Installation

### Prerequisites
Ensure you have Python installed (version 3.x recommended). You will also need **Pygame**.

To install Pygame, use:
```bash
pip install pygame
```

### Running the Program
Clone this repository and navigate to the project directory:
```bash
git clone https://github.com/eashwar910/maze-solver.git
cd maze-solver
```
Run the script:
```bash
python main.py
```

## How It Works
1. The maze is generated using **Kruskal's Algorithm**, ensuring a fully connected and solvable structure.
2. The user can select a search algorithm to solve the maze.
3. The algorithm will traverse the maze from the start to the end, visualizing the steps in real time.

## Algorithms Explained
### 1. Breadth-First Search (BFS)
- Explores all neighbors at the current depth before moving to the next level.
- Guarantees the shortest path.

### 2. Depth-First Search (DFS)
- Explores as deep as possible before backtracking.
- Does not guarantee the shortest path.

### 3. A* Search
- Uses a heuristic function (e.g., Manhattan distance) to prioritize paths.
- Guarantees the shortest path if an admissible heuristic is used.

### 4. Greedy Best-First Search
- Selects paths based on a heuristic function without considering the cost.
- Faster but does not always find the shortest path.

## Controls
- Use keyboard/mouse (if applicable) to navigate/select algorithms.
- Watch the algorithm in action as it solves the maze visually.


