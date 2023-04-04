import random

class Player:
    def __init__(self, color):
        self.color = self.determinecolor(color)
        self.oppcolor = self.determinecolor(self.color)
        self.moves = []
        self.enemy = self.ae(self.oppcolor)
        self.ally = self.ae(self.color)
        self.opponentmoves = []

class Random_player(Player):
    def next_move(self, board, opponent):
        self.opponentmoves = []
        return random.choice(self.moves)
