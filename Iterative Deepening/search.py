import puzzle8
import heapq


# Returns the number of misplaced tiles for the indicated state. The blank square does not count as a misplaced tile. It isn't a tile
def numWrongTiles(state):
    orderedNums = [0, 1, 2, 5, 8, 7, 6, 3]
    wrongTiles = 0
    for i in range(8):
        if puzzle8.getTile(state, orderedNums[i]) != i + 1:
            wrongTiles += 1

    return wrongTiles


# Returns number of moves required to get from square a to b.
def getDist(a, b):
    if b == () or a == b:
        return 0
    else:
        up = abs(a[0] - b[0])
        right = abs(a[1] - b[1])
    return up + right


# Returns the Manhattan distance for the misplaced tiles for the indicated state: for each tile,
# if you could slide it right through other tiles, measure the number of steps it would take
# to get it to the right place; then add those up. The blank square does not count as a misplaced tile.
def manhattanDistance(state):
    rightCoords = [(), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
    dist = 0
    for i in range(9):
        dist += getDist(puzzle8.xylocation(i), rightCoords[puzzle8.getTile(state, i)])

    return dist


class HeapItem:
    def __init__(self, state, steps, parent):
        self.state = state
        self.steps = steps
        self.value = steps + manhattanDistance(state)
        self.parent = parent

    def __cmp__(self, other):
        '''__cmp__ is supposed to return a negative number if self is
        "smaller" than other, 0 if equal, and a positive number if
        "greater."'''
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        return 1


def dfs(depth, state, dict):
    solution = None
    if dict == {}:
        dict[state] = None
    if state == puzzle8.solution():
        return state
    if depth == 0:
        return None

    for neighbor in puzzle8.neighbors(puzzle8.blankSquare(state)):
        possMove = puzzle8.moveBlank(state, neighbor)
        if possMove not in dict.keys():
            dict[possMove] = state
        solution = dfs(depth - 1, possMove, dict)
        if solution is not None:
            return solution


def itdeep(state):
    solution = None
    stack = []
    maxDepth = 0
    while solution is None:
        dict = {}
        solution = dfs(maxDepth, state, dict)
        maxDepth += 1

    while solution is not None:
        stack.append(puzzle8.blankSquare(solution))
        solution = dict[solution]
    stack = stack[:-1]
    stack.reverse()
    return stack


def astar(state, heuristic):
    myHeap = []
    solution = None
    stack = []

    if state == puzzle8.solution():
        return []
    if not myHeap:
        newFirst = HeapItem(state, 0, None)
        heapq.heappush(myHeap, newFirst)

    while solution is None:
        curr = heapq.heappop(myHeap)
        if curr.state == puzzle8.solution():
            solution = curr

        for neighbor in puzzle8.neighbors(puzzle8.blankSquare(curr.state)):
            possMove = puzzle8.moveBlank(curr.state, neighbor)
            newNeighbor = HeapItem(possMove, 1 + curr.steps, curr)
            heapq.heappush(myHeap, newNeighbor)

    while solution is not None:
        stack.append(puzzle8.blankSquare(solution.state))
        solution = solution.parent

    stack = stack[:-1]
    stack.reverse()
    return stack

goal = puzzle8.randomState()