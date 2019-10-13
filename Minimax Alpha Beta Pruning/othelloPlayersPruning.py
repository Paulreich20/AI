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
    corners = [(1,1), (1,8),(8,1),(8,8)]
    bad = [(1,2),(2,2),(2,1),(1,7),(2,7),(2,8),(7,1),(7,2),(8,2),(8,7),(7,7),(7,8)]
    ## TO DO DICTIONARIES


    # Dictionary contains key representing coordinates of speciic spots on the Othello board and values corresponding
    # to how good that spot is
    dict = {(1,1):10, (1,8):10,(8,1):10,(8,8):10,
            (1,2):-2,(2,2):-2,(2,1):-2,
            (1,7):-2,(2,7):-2,(2,8):-2,(7,1):-2,
            (7,2):-2,(8,2):-2,(8,7):-2, (7, 7): -2,(7, 8): -2}

    sum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1, othelloBoard.size-1):
            if (i, j) in dict.keys():
                mult = dict[(i, j)]
            #Consider outermost edges to be better than average choice and spots that allow oppoent to place a piece
            # on outermost edges to be worse than average
            elif i == 2 or i == 7 or j == 2 or j == 7:
                mult = -1
            elif i == 1 or i == 8 or j == 1 or j == 8:
                mult = 3
            else:
                mult = 1
            sum += board.array[i][j]*mult

    # Improve heuristic if player has more mobility than opponent
    netLegalMoves = len(board.legalMoves(1)) - len(board.legalMoves(-1))
    sum += 3.14*netLegalMoves

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

        # Establish reset value to best, use to find min/max of children
        if self.color == -1:
            best = 99999
        else:
            best = -99999
        nextMove = (0, 0, 0)

        # Pass if no legal moves
        if not board.legalMoves(self.color):
            return None

        # Run depth first search on all legal moves, using minimax
        for move in board.legalMoves(self.color):
            bcopy = board.makeMove(move[0], move[1], self.color)
            if self.color == -1:
                temp = self.minValue(bcopy, self.plies-1, self.color*-1)
                if temp <= best:
                    best = temp
                    nextMove = move

            else:
                temp = self.maxValue(bcopy, self.plies-1, self.color*-1)
                if temp >= best:
                    best = temp
                    nextMove = move

        return (nextMove[0], nextMove[1], self.heuristicCalls)

    def maxValue(self, board, ply, color):
        if not board.legalMoves(-1) and not board.legalMoves(1):
            score = board.scores()[1] - board.scores()[0]
            if score == 0:
                return 0
            if (color == -1 and score < 0) or (color == 1 and score < 0):
                return -9999
            if (color == 1 and score > 0) or (color == -1 and score > 0):
                return 9999

        elif ply == 0:
            self.heuristicCalls += 1
            return self.heuristic(board)
        else:
            best = -9999
            for move in board.legalMoves(color):
                nextMove = board.makeMove(move[0], move[1], color)
                best = max(best, self.minValue(nextMove, ply-1, color*-1))
            return best

    def minValue(self, board, ply, color):
        if not board.legalMoves(-1) and not board.legalMoves(1):
            score = board.scores()[1] - board.scores()[0]
            if score == 0:
                return 0
            if (color == -1 and score < 0) or (color == 1 and score < 0):
                return -9999
            if (color == 1 and score > 0) or (color == -1 and score > 0):
                return 9999

        elif ply == 0:
            self.heuristicCalls += 1
            return self.heuristic(board)
        else:
            best = 9999
            for move in board.legalMoves(color):
                nextMove = board.makeMove(move[0], move[1], color)
                best = min(best, self.maxValue(nextMove, ply-1, color*-1))
            return best

class ComputerPlayerPruning:
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
        if self.color == -1:
            best = 99999
        else:
            best = -99999

        nextMove = (0, 0, 0)

        if not board.legalMoves(self.color):
            return None

        for move in board.legalMoves(self.color):
            bcopy = board.makeMove(move[0], move[1], self.color)
            if self.color == -1:
                temp = self.minValue(bcopy, self.plies-1, self.color*-1, -999999, 999999)
                if temp <= best:
                    best = temp
                    nextMove = move

            else:
                temp = self.maxValue(bcopy, self.plies-1, self.color*-1, -999999, 999999)
                if temp >= best:
                    best = temp
                    nextMove = move

        return (nextMove[0], nextMove[1], self.heuristicCalls)

    def maxValue(self, board, ply, color, alpha, beta):
        if not board.legalMoves(-1) and not board.legalMoves(1):
            score = board.scores()[1] - board.scores()[0]
            if score == 0:
                return 0
            if (color == -1 and score < 0) or (color == 1 and score < 0):
                return -9999
            if (color == 1 and score > 0) or (color == -1 and score > 0):
                return 9999

        elif ply == 0:
            self.heuristicCalls += 1
            return self.heuristic(board)
        else:
            best = -9999
            for move in board.legalMoves(color):
                nextMove = board.makeMove(move[0], move[1], color)
                best = max(best, self.minValue(nextMove, ply - 1, color*-1, alpha, beta))
                if best >= beta:
                    return best
                alpha = max(alpha, best)
            return best

    def minValue(self, board, ply, color, alpha, beta):
        if not board.legalMoves(-1) and not board.legalMoves(1):
            score = board.scores()[1] - board.scores()[0]
            if score == 0:
                return 0
            if (color == -1 and score < 0) or (color == 1 and score < 0):
                return -9999
            if (color == 1 and score > 0) or (color == -1 and score > 0):
                return 9999

        elif ply == 0:
            self.heuristicCalls += 1
            return self.heuristic(board)
        else:
            best = 9999
            for move in board.legalMoves(color):
                nextMove = board.makeMove(move[0], move[1], color)
                best = min(best, self.maxValue(nextMove, ply - 1, color*-1, alpha, beta))
                if best <= alpha:
                    return best
                beta = min(beta, best)
            return best






