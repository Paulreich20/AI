'''This is a direct port, by Dave Musicant, of some of the original
Lisp code for the 8-puzzle by Russell & Norvig. Much of the comments
are copied verbatim.

DO NOT MODIFY THIS CODE. We will grade your assignment based on this
code, exactly as it is written, and your own additional submission
that uses it.

DO NOT MODIFY THIS CODE.

In this implementation of the 8-puzzle we have a mix of priorities
between efficiency and simplicity.  We restrict ourselves to the
8-puzzle, instead of the general n-puzzle.  The representation of
states is not the obvious one (a 3x3 array), but it is both
efficient and fairly easy to manipulate.  We represent each tile
as an integer from 0 to 8 (0 for the blank).  We also represent
each square as an integer from 0 to 8, arranged as follows:

    0 1 2
    3 4 5
    6 7 8

Finally, we represent a state (i.e., a complete puzzle) as the sum
of the tile numbers times 9 to the power of the tile square number.
For example, the goal state from page 63:

    1 2 3                          1*9^0 + 2*9^1 + 3*9^2
    8 . 4  is represented by:    + 8*9^3 + 0*9^4 + 4*9^5
    7 6 5                        + 7*9^6 + 6*9^7 + 5*9^8 = 247893796
'''

import random

def state(pieces):
    '''Define a new state with the tile number indicated in each
    position (use 0 for blank). Parameter should be a list of nine digits.'''
    if len(pieces) != 9:
        raise Exception("List should be of size 9")
    sum = 0
    for i in range(9):
        sum += pieces[i] * 9**i
    return sum

# Puzzle goal
_goal = state([1,2,3,8,0,4,7,6,5])


def moveBlank(state,dest):
    '''Move the blank from one square to another and return the
    resulting state. Raises an exception if the move is not legal.'''
    class IllegalMoveException(Exception):
        pass

    source = blankSquare(state)
    if not(dest in neighbors(source)):
        raise IllegalMoveException
    return state + getTile(state,dest) * (_power9(source) - _power9(dest))

def blankSquare(state):
    '''Find the number of the square where the blank is.'''
    for i in range(9):
        if getTile(state,i) == 0:
            return i

def randomState(numMoves=100):
    '''Produces a random puzzle by randomly sliding puzzle pieces
    around numMoves number of times. The goal state (where this starts
    from) is assumed to be the goal in the textbook, i.e.
       1 2 3
       8 . 4
       7 6 5'''
    
    state = _goal
    for _ in range(numMoves):
        choices = list(neighbors(blankSquare(state)))
        state = moveBlank(state, choices[random.randint(0,len(choices)-1)])
    return state



def neighbors(square):
    '''The squares that can be reached from a given square. The
    parameter "square" is a number from 0 to 8.'''
    class IllegalSquareException(Exception):
        pass
    if square < 0 or square > 8:
        raise IllegalSquareException(square)

    # Tuples are being used here instead of lists to prevent accidental
    # modification later. These should be fixed.
    return [(1,3),
            (0,2,4),
            (1,5),
            (0,4,6),
            (1,3,5,7),
            (2,4,8),
            (3,7),
            (4,6,8),
            (5,7)][square]

def getTile(state,square):
    "Return the tile that occupies the given square."
    return (state // _power9(square)) % 9

def display(state):
    '''Display the puzzle associated with the given state.'''
    for i in range(9):
        tile = getTile(state,i)
        if tile==0:
            print('.',end=' ')
        else:
            print(tile,end=' ')
        if (i+1)%3==0:
            print()
            
def _power9(n):
    '''Raise 9 to the nth power, 0 <= n <= 9.'''
    # This is likely considerably faster than 9**n.
    return [1,9,81,729,6561,59049,531441,4782969,43046721,387420489][n]

def xylocation(square):
    '''Return the (x y) location of a square number, where x
    represents the column number, and y represents the row number.'''
    return [(0, 0), (1, 0), (2, 0),
            (0, 1), (1, 1), (2, 1),
            (0, 2), (1, 2), (2, 2)][square]

def solution():
    '''Returns the state corresponding to the solution.'''
    return _goal
    

########################################
# Unit tests
########################################

import unittest
class _TestMethods(unittest.TestCase):

    def testState(self):
        self.assertEqual(state([1,2,3,8,0,4,7,6,5]),247893796)

    def testGetTile(self):
        self.assertEqual(getTile(247893796,0),1)
        self.assertEqual(getTile(247893796,3),8)

    def testBlankSquare(self):
        self.assertEqual(blankSquare(247893796),4)

    def testMoveBlank(self):
        state1 = state([1,2,3,8,0,4,7,6,5])
        state2 = state([1,0,3,8,2,4,7,6,5])
        self.assertEqual(moveBlank(state1,1),state2)
    
    def testNeighbors(self):
        self.assertSetEqual(set(neighbors(4)),set([1,3,7,5]))

    def testSolution(self):
        self.assertEqual(state([1,2,3,8,0,4,7,6,5]),solution())

    def testXylocation(self):
        self.assertEqual(xylocation(5),(2,1))

    def testRandomState(self):
        self.assertEqual(randomState(0),solution())
        random.seed(12345)
        self.assertEqual(randomState(1),state([1,2,3,8,6,4,7,0,5]))
        random.seed(12345)
        self.assertEqual(randomState(100),108261756)


if __name__=='__main__':
    unittest.main()
