# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]



"""First 4 search algorithms have similar structure but use different data structures for frontier"""
def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    from util import Stack
    
    frontier = Stack()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0))  # (state, path, depth)
    explored = set()
    
    nodes_expanded = 0
    max_depth = 0
    
    while not frontier.isEmpty():
        currentState, actions, depth = frontier.pop()
        
        if currentState in explored:
            continue
        
        explored.add(currentState)
        nodes_expanded += 1
        max_depth = max(max_depth, depth)
        
        if problem.isGoalState(currentState):
            return actions, nodes_expanded, max_depth  # Found 
        
        successors = problem.getSuccessors(currentState)
        
        for nextState, action, cost in successors:
            if nextState not in explored:
                newActions = actions + [action]
                frontier.push((nextState, newActions, depth + 1))
    
    return [], nodes_expanded, max_depth # No solution found
        

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    
    frontier = Queue()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0))  # (state, path, depth)
    explored = set()
    
    nodes_expanded = 0
    max_depth = 0
    
    while not frontier.isEmpty():
        currentState, actions, depth = frontier.pop()
        
        if currentState in explored:
            continue
        
        explored.add(currentState)
        nodes_expanded += 1
        max_depth = max(max_depth, depth)
        
        if problem.isGoalState(currentState):
            return actions, nodes_expanded, max_depth  # Found 
        
        successors = problem.getSuccessors(currentState)
        
        for nextState, action, cost in successors:
            if nextState not in explored:
                newActions = actions + [action]
                frontier.push((nextState, newActions, depth + 1))
    
    

#explained by https://github.com/mgabilo/eightpuzzle-iterative-deepening

def iterativeDeepeningSearch(problem: SearchProblem):
    
    from util import Stack
    
    total_nodes_expanded = 0
    depth_limit = 0
    
    while True:
        # Do depth-limited DFS
        result, nodes_expanded = depthLimitedDFS(problem, depth_limit)
        total_nodes_expanded += nodes_expanded
        
        if result != 'cutoff':
            return result, total_nodes_expanded, depth_limit
        
        # Otherwise, increase depth limit and try again
        depth_limit += 1
    


def depthLimitedDFS(problem: SearchProblem, limit):
    #utility for IDS
    from util import Stack   
     
    frontier = Stack()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0))  # (state, actions, depth)
    explored = set()
    
    nodes_expanded = 0
    cutoff_occurred = False
    
    while not frontier.isEmpty():
        currentState, actions, depth = frontier.pop()
        
        # Skip if already visited at this or shallower depth
        if currentState in explored:
            continue
        
        explored.add(currentState)
        nodes_expanded += 1
        
        # Goal test
        if problem.isGoalState(currentState):
            return actions, nodes_expanded
        
        if depth < limit:
            successors = problem.getSuccessors(currentState)
            
            for nextState, action, cost in successors:
                if nextState not in explored:
                    newActions = actions + [action]
                    frontier.push((nextState, newActions, depth + 1))
        else:
            # Hit the depth limit - this path is cut off
            cutoff_occurred = True
    
    # If we cut off any paths, signal that we should try deeper
    if cutoff_occurred:
        return 'cutoff', nodes_expanded
    else:
        return [], nodes_expanded  # No solution 


#uses function getcostofactions from eightpuzzle
def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    frontier = PriorityQueue()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), 0)  # ((state, actions, depth), priority=cost)
    explored = set()
    
    nodes_expanded = 0
    max_depth = 0
    
    while not frontier.isEmpty():
        currentState, actions, depth = frontier.pop()
        
        if currentState in explored:
            continue
        
        explored.add(currentState)
        nodes_expanded += 1
        max_depth = max(max_depth, depth)
        
        if problem.isGoalState(currentState):
            return actions, nodes_expanded, max_depth
        
        # Expand successors
        successors = problem.getSuccessors(currentState)
        
        for nextState, action, stepCost in successors:
            if nextState not in explored:
                newActions = actions + [action]
                newCost = problem.getCostOfActions(newActions)
                frontier.push((nextState, newActions, depth + 1), newCost)
    
    return [], nodes_expanded, max_depth

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    frontier = PriorityQueue()
    start_state = problem.getStartState()
    start_heuristic = heuristic(start_state, problem)
    frontier.push((start_state, [], 0), start_heuristic)  
    explored = set()

    nodes_expanded = 0
    max_depth = 0

    while not frontier.isEmpty():
        currentState, actions, depth = frontier.pop()

        if currentState in explored:
            continue

        explored.add(currentState)
        nodes_expanded += 1
        max_depth = max(max_depth, depth)

        if problem.isGoalState(currentState):
            return actions, nodes_expanded, max_depth

        successors = problem.getSuccessors(currentState)

        for nextState, action, stepCost in successors:
            if nextState not in explored:
                newActions = actions + [action]
                actual_cost = problem.getCostOfActions(newActions)
                next_heuristic = heuristic(nextState, problem)
                priority = actual_cost + next_heuristic
                frontier.push((nextState, newActions, depth + 1), priority)
            
    return [], nodes_expanded, max_depth

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
