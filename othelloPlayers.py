import othelloBoard
from typing import Tuple, Optional

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the heuristic function, which should
return a number indicating the value of that board position (the
bigger the better). We will use your heuristic function when running
the tournament between players.

Feel free to add additional methods or functions.'''

class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                print('Illegal entry, try again.')
            except Exception:
                print('Illegal entry, try again.')

        if move==(0,0):
            return None
        else:
            return move

def heuristic(board) -> int:
    '''This very silly heuristic just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''

    # If board is an end game state, don't need heuristic, give scores
    if not board.legalMoves("black") and not board.legalMoves("white"): ## <------------- CHANGE THIS TO REFLECT ACTUAL COLOR
        return board.scores()[0]
    else:
        sum = 0
        for i in range(1,othelloBoard.size-1):
            for j in range(1,othelloBoard.size-1):
                sum += board.array[i][j]
    return sum


    

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies) -> None:
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies
        self.heuristicCalls = 0


    # chooseMove should return a tuple that looks like:
    # (row of move, column of move, number of times heuristic was called)
    # We will be using the third piece of information to assist with grading.
    def chooseMove(self,board) -> Optional[Tuple[int,int,int]]:
        '''This very silly player just returns the first legal move
        that it finds.'''
        self.heuristicCalls = 0
        best = 0
        nextMove = (0, 0, 0)
        if board.legalMoves(self.color):
            return (0, 0, 0)

        for move in board.legalMoves(self.color):
            bcopy = board.makeMove(move[0], move[1], self.color)
            if self.color == "black":
                temp = self.minValue(bcopy, self.plies)
                if temp <= best:
                    best = temp
                    nextMove = move

            else:
                temp = self.maxValue(bcopy, self.plies)
                if temp >= best:
                    best = temp
                    nextMove = move

        return (nextMove[0], nextMove[1], self.heuristicCalls)

    def maxValue(self, board, ply):
        if not board.legalMoves(self.color):
            if self.color == "black":
                return board.scores()[0]
            return board.scores()[1]

        elif ply == 0:
            self.heuristicCalls += 1
            return self.heuristic(board)
        else:
            best = -9999
            for move in board.legalMoves(self.color):
                nextMove = board.makeMove(move[0], move[1], self.color)
                best = max(best, self.minValue(nextMove, ply-1))
            return best

    def minValue(self, board, ply):
        if not board.legalMoves(self.color):
            if self.color == "black":
                return board.scores()[0]
            return board.scores()[1]
        elif ply == 0:
            self.heuristicCalls += 1
            return self.heuristic(board)
        else:
            best = 9999
            for move in board.legalMoves(self.color):
                nextMove = board.makeMove(move[0], move[1], self.color)
                best = min(best, self.maxValue(nextMove, ply-1))
            return best




