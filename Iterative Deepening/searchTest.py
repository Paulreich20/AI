# Some tests  for the functions  that you write. Notice  that the tests  for the
# search algorithms are terrible; my real goal  here is simply to make sure that
# you have followed  instructions, so that we can grade  it more easily. Passing
# these  tests definitely  does  not mean  that you  have  implemented the  code
# correctly. We will test more carefully when grading; you should too.

# Version 1.1: Corrected tests for randomState(1) in the two heuristics.

import unittest
import puzzle8
import search
import random

class TestMethods(unittest.TestCase):

    offTwoPuzzle = puzzle8.state([3,4,5,2,0,6,1,8,7])

    def testNumWrongTiles(self):
        self.assertEqual(search.numWrongTiles(puzzle8.solution()),0)
        self.assertEqual(search.numWrongTiles(puzzle8.randomState(1)),1)
        self.assertEqual(search.numWrongTiles(self.offTwoPuzzle),8)

    def testManhattanDistance(self):
        self.assertEqual(search.manhattanDistance(puzzle8.solution()),0)
        self.assertEqual(search.manhattanDistance(puzzle8.randomState(1)),1)
        self.assertEqual(search.manhattanDistance(self.offTwoPuzzle),16)

    def testItdeep(self):
        self.assertEqual(search.itdeep(puzzle8.solution()),[])
        self.assertEqual(len(search.itdeep(puzzle8.randomState(1))),1)
        testPuzzle = puzzle8.state([1,2,0,8,6,3,7,5,4])
        self.assertEqual(search.itdeep(testPuzzle),[5,8,7,4])

        random.seed(12345)
        randomMoves = 32
        testPuzzle2 = puzzle8.randomState(randomMoves)
        puzzle8.display(testPuzzle2)
        solnPath = search.itdeep(testPuzzle2)
        self.assertLessEqual(len(solnPath),randomMoves)

    def testAstar(self):
        random.seed(12345)
        randomMoves = 32
        testPuzzle2 = puzzle8.randomState(randomMoves)
        puzzle8.display(testPuzzle2)
        solnPath = search.astar(testPuzzle2, search.manhattanDistance)
        self.assertLessEqual(len(solnPath),randomMoves)
        
if __name__=='__main__':
    unittest.main()
