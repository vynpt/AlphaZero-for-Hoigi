import random
import numpy
from copy import deepcopy

class Player:
    def __init__(self, team):
        ## team = 1 or -1, 1 for white, -1 for black
        self.team = team
        self.opponent_team = team * -1
        self.moves = []
        self.opponentmoves = []

    def add_move(self, board, opponent):
        self.moves = board.legal_moves(self.team)
    
    def next_move(self, board, opponent):
        # by default the play class makes random moves
        self.add_move(board, opponent)
        #print("player moves", self.moves)
        result = random.choice(self.moves) 
        self.clear_moves() # clears the move so future moves are not disrupted
        return result
    
    def clear_moves(self):
        # modifier method for clearing moves
        self.moves = []

    def check_turn(self, board):
        # helper function for checking if it is the player's turn
        if (board.turn != self.team):
            print("Not this player's turn Error!")
            return False
        else:
            return True

class AlphaBetaMinimaxAI(Player):
    
    def __init__(self, color):
        super().__init__(color)
        self.MAX = 1000
        self.MIN = -1000

    # Returns optimal value for current player
    #(Initially called for root and maximizer)
    def minimax(self, depth, nodeIndex, maximizingPlayer,
                values, alpha, beta):
    
        # Terminating condition. i.e
        # leaf node is reached
        if depth == 3:
            return values[nodeIndex]
    
        if maximizingPlayer:
        
            best = self.MIN
    
            # Recur for left and right children
            for i in range(0, 2):
                
                val = self.minimax(depth + 1, nodeIndex * 2 + i,
                            False, values, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
    
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            
            return best
        
        else:
            best = self.MAX
    
            # Recur for left and
            # right children
            for i in range(0, 2):
            
                val = self.minimax(self, depth + 1, nodeIndex * 2 + i,
                                True, values, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
    
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            
            return best
        
    def test(self):
        values = [3, 5, 6, 9, 1, 2, 0, -1] 
        print("The optimal value is :", self.minimax(0, 0, True, values, self.MIN, self.MAX))

class Minimax_Player(Player): 
    def eval_board(self, board):
        # Heuristic function for minimax
        # Don't question, we just made this up
        score = 0
        pieces = board.allpieces()
        for p in pieces:
            score += p[0].value[p[0].type]
        return score

    def min_maxN(self, board,n):
        # requires that self.moves contains legal moves available for the current player
        scores = []   ## scoring for each move, positive is good for white, negative is good for black
        moves = []
        
        for move in self.moves:
            # make copy of the board position so we are not changing the actual board when trying moves
            temp = deepcopy(board)
            temp.push(move)

            if n>0:  # look ahead n moves opponent player plays
                temp_best_move = self.min_maxN(temp,n-1)
                temp.push(temp_best_move)

            scores.append(self.eval_board(temp))   # score corresponse to the move indices

        if self.team == 1:
            best_move = self.moves[scores.index(max(scores))] # max() finds the highest positive score
        else: # that is self.team == -1
            best_move = self.moves[scores.index(min(scores))] # min() finds the lowest positive score

        return best_move
    
    def next_move(self, board, opponent):
        self.add_move(board, opponent)
        print("available moves", self.moves)
        self.clear_moves()
        return self.min_maxN(board, 1)
        
# a simple wrapper function as the display only gives one imput , board
#def play_min_maxN(board):
#    N=3
#    return min_maxN(board,N)