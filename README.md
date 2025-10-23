# Eight Puzzle Search Algorithms

Implementation of search algorithms (DFS, BFS, IDS, UCS, GBS, A*) for the Eight Puzzle problem.

## Quick Start

**Location:** All code is in `PA1_Search/Code/`

**Run from:** `PA1_Search/Code` directory

```bash
cd PA1_Search/Code
```

## Running Algorithms

### Uninformed Search (no heuristic needed)
```bash
# Breadth-First Search
python3 eightpuzzle.py --search BFS --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]'

# Depth-First Search
python3 eightpuzzle.py --search DFS --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]'

# Iterative Deepening Search
python3 eightpuzzle.py --search IDS --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]'

# Uniform Cost Search
python3 eightpuzzle.py --search UCS --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]'
```

### Informed Search (requires `--heuristic`)
```bash
# A* with Manhattan Distance
python3 eightpuzzle.py --search Astar --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]' --heuristic manhattan

# A* with Misplaced Tiles
python3 eightpuzzle.py --search Astar --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]' --heuristic misplaced

# Greedy Best-First Search with Manhattan
python3 eightpuzzle.py --search GBS --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]' --heuristic manhattan

# Greedy Best-First Search with Misplaced Tiles
python3 eightpuzzle.py --search GBS --initial '[[1,-,2],[3,4,5],[6,7,8]]' --goal '[[1,2,3],[4,5,6],[7,8,-]]' --heuristic misplaced
```


## Output Files

**Each algorithm run creates a `.txt` file** in `PA1_Search/Code/` showing the complete solution:

**Each file contains:**
- Initial and goal states
- Complete solution path (step-by-step moves)
- Performance metrics (moves, nodes expanded, depth, runtime)

## Code Files

- `PA1_Search/Code/eightpuzzle.py` — Problem definition and CLI
- `PA1_Search/Code/search.py` — All search algorithms and heuristics
- `PA1_Search/Code/util.py` — Data structures (Stack, Queue, PriorityQueue)

