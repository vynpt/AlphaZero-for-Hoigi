from Hoigi_Pieces import *
class board:
    """ game board for chess
    """
    def __init__(self, height, width, layers):
        """ constructs a new board object
        """
        # definition of a move and its format:
        # [piece.team, piece.type, destination location, original position, capture (False for no capture, True for capture)

        self.height = height
        self.width = width
        self.layers = layers
        self.squares = [[[' ' for i in range(self.layers)] for j in range(self.height)] for k in range(self.width)] # always in the form of [rows, columns, layers]
        self.previous_move = []

        self.move_history = []

        # data format of position 9x9x3 x9, p is number of pieces 
        # 0 = empty square, 1 = white, -1 = black
        self.dataformat = [[[[0 for i in range(self.layers)] for j in range(self.height)] for k in range(self.width)] for p in range(9)] 
        
    def __repr__(self):             #  representation without graphics
        """ Returns a string representation for a Board object.
        """
        s = ""
        for y in range(self.height):
            s += "--" * self.width + "-" + "\n"
            s += "|"
            for x in range(self.width):
                s += "(" + self.squares[y][x][2] + "," + self.squares[y][x][1] + "," + self.squares[y][x][0] + ")" + "|"
            s += "\n"
        s += "--" * self.width + "-" + "\n"
        return s

    def copy_board(self):
        """ create and return a copy of the board object
        """
        y = self.height
        x = self.width
        z = self.layers
        newboard = board(y, x, z)
        for row in range(y):
            for column in range(x):
                for layer in range(z):
                    newboard.squares[row][column][layer] = self.squares[row][column][layer]
        return newboard

    def add_piece(self, team, type, image, destination, capture):
        """ add a piece to a specified square on the Board
            team = 1 or -1
            type = integer representation of piece
            image = .png image for piece
            destination = [y,x,z] position on board
            capture = boolean

        """
        p = Piece(team, type, image)
        self.squares[destination[0]][destination[1]][destination[2]] = p

    def remove_piece(self, original, capture):
        """ remove a piece from a specified square on the Board
            original = [y,x,z] position of the piece on board 
        """
        self.squares[original[0]][original[1]][original[2]] = " "
        
    def check_winner(self):
        # return an integer, 0 = no winner, -1 = black is winner, 1 = white is winner
        winner = 0    
        for y in range(self.height):
            for x in range(self.width):
                if (self.squares[y][x][2].type == 2 and self.squares[y][x][2].team == 1):  # find white king
                    winner += 1
                if (self.squares[y][x][2].type == 2 and self.squares[y][x][2].team == -1):  # find black king
                    winner -= 1
        return winner
    
    def allpieces(self):
        # return a list of all pieces on the board, and the position they are at in [y,x,z] format
        list = []
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.layers):
                    if (self.squares[y][x][z] != " "):
                        list += [self.squares[y][x][z], [y,x,z]]
        return list

    def legal_moves(self, team):
        # return a list of all legal moves for a team
        movelist = []
        for [p, position] in self.allpieces():
            if (p.team == team):
                movelist += p.moves(board, position)
        return movelist 