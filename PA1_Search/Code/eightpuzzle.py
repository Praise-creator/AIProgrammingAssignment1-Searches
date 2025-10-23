# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import search
import random
import argparse
import time
import json

# Module Classes

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range( 3 ):
            self.cells.append( [] )
            for col in range( 3 ):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range( 3 ):
            for col in range( 3 ):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 2):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 2):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range( 3 ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class EightPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self,puzzle, goal = None):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle
        
        #custom goal state
        if goal is None:
            self.goal = EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8])
        else:
            self.goal = goal


    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state == self.goal

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    """
      puzzleNumber: The number of the eight puzzle to load.

      Returns an eight puzzle object generated from one of the
      provided puzzles in EIGHT_PUZZLE_DATA.

      puzzleNumber can range from 0 to 5.

      >>> print(loadEightPuzzle(0))
      -------------
      | 1 |   | 2 |
      -------------
      | 3 | 4 | 5 |
      -------------
      | 6 | 7 | 8 |
      -------------
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])

def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = EightPuzzleState([0,1,2,3,4,5,6,7,8])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

def parse_grid(grid_string):
    # First replace '-' with '0' to make it valid JSON
    grid_string = grid_string.replace('-', '0')
    
    grid_string = grid_string.replace(' ', '')
    
    grid = json.loads(grid_string)
    
    numbers = []
    for row in grid:
        for cell in row:
            numbers.append(int(cell))
    
    return numbers



# Had claude generate this
def run_search(problem, search_func, search_name, initial_state, heuristic=None):
    """
    Generic function to run any search algorithm and track metrics.
    
    Args:
        problem: EightPuzzleSearchProblem instance
        search_func: The search function to call (e.g., search.depthFirstSearch)
        search_name: Name of the algorithm (e.g., 'DFS', 'BFS')
        initial_state: The initial puzzle state
        heuristic: Heuristic function (for informed search)
    """
    print(f"Running {search_name}...")
    
    start_time = time.time()
    
    # Call the search function (with or without heuristic)
    if heuristic:
        result = search_func(problem, heuristic)
    else:
        result = search_func(problem)
    
    end_time = time.time()
    
    # Unpack result (all search functions should return same format)
    path, nodes_expanded, max_depth = result
    
    return {
        'search_name': search_name,
        'path': path,
        'path_cost': len(path),
        'nodes_expanded': nodes_expanded,
        'max_depth': max_depth,
        'time': end_time - start_time,
        'initial_state': initial_state
    }

def write_output(metrics, problem, heuristic_name=None):
    """
    Generic function to write output for any search algorithm.
    Handles the naming convention based on search type and heuristic.
    """
    search_name = metrics['search_name']
    
    # Build filename according to assignment requirements
    safe_search_name = search_name.replace('*', 'star')
    
    if heuristic_name and search_name in ['GBS', 'A*']:
        filename = f"output_{safe_search_name}_{heuristic_name}.txt"
    else:
        filename = f"output_{safe_search_name}.txt"
    
    with open(filename, 'w') as f:
        # Write header
        f.write(f"{search_name}")
        if heuristic_name:
            f.write(f" (Heuristic: {heuristic_name})")
        f.write("\n")
        f.write("*" * 50 + "\n\n")
        
        # Write path
        f.write("Path:\n")
        f.write("=" * 50 + "\n\n")
        
        current_state = metrics['initial_state']
        f.write("Initial State (s0):\n")
        f.write(str(current_state) + "\n\n")
        
        if len(metrics['path']) == 0:
            f.write("No solution found!\n\n")
        else:
            for i, action in enumerate(metrics['path'], 1):
                current_state = current_state.result(action)
                f.write(f"Step {i}: Action = '{action}' -> State (s{i}):\n")
                f.write(str(current_state) + "\n\n")
            
            f.write(f"Goal State (s{len(metrics['path'])}) reached!\n\n")
        
        f.write("=" * 50 + "\n")
        f.write("Path Sequence:\n")
        if len(metrics['path']) > 0:
            path_str = " -> ".join(metrics['path'])
            f.write(f"{path_str}\n\n")
        else:
            f.write("No path found\n\n")
        
        f.write("=" * 50 + "\n")
        f.write("METRICS:\n")
        f.write("=" * 50 + "\n")
        f.write(f"Path Cost: {metrics['path_cost']}\n")
        f.write(f"Nodes Expanded: {metrics['nodes_expanded']}\n")
        f.write(f"Search Depth: {metrics['max_depth']}\n")
        f.write(f"Time Taken: {metrics['time']:.6f} seconds\n")
        f.write("=" * 50 + "\n")
    
    print(f"\nResults written to {filename}")
    print(f"Path Cost: {metrics['path_cost']}")
    print(f"Nodes Expanded: {metrics['nodes_expanded']}")
    print(f"Search Depth: {metrics['max_depth']}")
    print(f"Time Taken: {metrics['time']:.6f} seconds")
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve 8-Puzzle using various search algorithms')
    parser.add_argument('--search', type=str, required=True,
                       choices=['BFS', 'DFS', 'IDS', 'UCS', 'GBS', 'A*', 'Beam'],
                       help='Search algorithm to use')
    parser.add_argument('--initial', type=str, required=True,
                       help='Initial state as a 2D grid, e.g., "[[-,2,3],[1,4,5],[8,7,6]]"')
    parser.add_argument('--goal', type=str, required=True,
                       help='Goal state as a 2D grid, e.g., "[[1,2,3],[8,-,4],[7,6,5]]"')
    parser.add_argument('--heuristic', type=str, default='misplaced',
                       choices=['misplaced', 'manhattan', 'other'],
                       help='Heuristic function for informed search')
    
    args = parser.parse_args()
    
    # Parse initial and goal states
    print("Parsing input...")
    initial_numbers = parse_grid(args.initial)
    goal_numbers = parse_grid(args.goal)
    
    # Create puzzle states
    puzzle = EightPuzzleState(initial_numbers)
    goal = EightPuzzleState(goal_numbers)
    
    print("\nInitial puzzle:")
    print(puzzle)
    print("\nGoal puzzle:")
    print(goal)
    
    # Create search problem with custom goal
    problem = EightPuzzleSearchProblem(puzzle, goal)
    
    # Run selected search algorithm
    metrics = None
    heuristic_func = None
    
    if args.search == 'DFS':
        metrics = run_search(problem, search.depthFirstSearch, 'DFS', puzzle)
        write_output(metrics, problem)
        
    elif args.search == 'BFS':
        metrics = run_search(problem, search.breadthFirstSearch, 'BFS', puzzle)
        write_output(metrics, problem)
        
    elif args.search == 'IDS':
        metrics = run_search(problem, search.iterativeDeepeningSearch, 'IDS', puzzle)
        write_output(metrics, problem)
        
    elif args.search == 'UCS':
        metrics = run_search(problem, search.uniformCostSearch, 'UCS', puzzle)
        write_output(metrics, problem)
        
    elif args.search == 'GBS':
        # Get heuristic function
        if args.heuristic == 'misplaced':
            heuristic_func = search.misplacedTilesHeuristic
        elif args.heuristic == 'manhattan':
            heuristic_func = search.manhattanDistanceHeuristic
        
        metrics = run_search(problem, search.greedyBestFirstSearch, 'GBS', puzzle, heuristic_func)
        write_output(metrics, problem, args.heuristic)
        
    elif args.search == 'A*':
        # Get heuristic function
        if args.heuristic == 'misplaced':
            heuristic_func = search.misplacedTilesHeuristic
        elif args.heuristic == 'manhattan':
            heuristic_func = search.manhattanDistanceHeuristic
        
        metrics = run_search(problem, search.aStarSearch, 'A*', puzzle, heuristic_func)
        write_output(metrics, problem, args.heuristic)
    
    print("\nSearch completed!")