import search
from eightpuzzle import EightPuzzleState, EightPuzzleSearchProblem

puzzle = EightPuzzleState([1,0,2,3,4,5,6,7,8])
print("Initial State:")
print(puzzle)
print()

problem = EightPuzzleSearchProblem(puzzle)

print("Performing Depth-First Search...")
path = search.depthFirstSearch(problem)
print('DFS found a path of %d moves: %s' % (len(path), str(path)))
curr = puzzle

for i,a in enumerate(path):
    curr = curr.result(a)
    print('After %d move%s: %s' % (i+1, ("", "s")[i>0], a))
    print(curr)
    print()