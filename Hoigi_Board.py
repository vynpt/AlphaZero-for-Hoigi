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
        self.squares = board = [[[' ' for i in range(self.layers)] for j in range(self.height)] for k in range(self.width)] # always in the form of [rows, columns, layers]
        self.previous_move = []

        self.move_history = []
        
# Capital letter for WHITE
# Lower case letter for BLACK
    def __repr__(self):             #  representation without graphics
        """ Returns a string representation for a Board object.
        """
        s = ""
        for y in range(self.height):
            s += "--" * self.width + "-" + "\n"
            s += "|"
            for x in range(self.width):
                s += "(" + self.squares[y][x][0] + "," + self.squares[y][x][1] + "," + self.squares[y][x][2] + ")" + "|"
            s += "\n"
        s += "--" * self.width + "-" + "\n"
        return s

    def copy_board(self):
        """ create and return a copy of the board object
        """
        y = self.height
        x = self.width
        newboard = board(y, x)
        for row in range(y):
            for column in range(x):
                newboard.squares[row][column] = self.squares[row][column]
        return newboard

    def add_piece(self, piece, destination, capture):
        """ add a chess piece to a specified square on the Board
            columns and rows are referred to as starting from the
            bottom left corner
        """
        if capture[0] == -2:
            return 0
        elif capture[0] == -3: #capture [rook, destination, original]
            self.squares[destination[1]][destination[0]] = piece
            self.squares[capture[1][1][1]][capture[1][1][0]] = capture[1][0]
        else:
            self.squares[destination[1]][destination[0]] = piece

    def remove_piece(self, original, capture):
        """ remove a chess piece from a specified square on the Board
        """
        if (capture[0] == -1):
            self.squares[original[1]][original[0]] = " "
        elif (capture[0] == -2):
            self.squares[original[1]][original[0]] = " "
            pass
        elif (capture[0] == -3):
            self.squares[capture[1][2][1]][capture[1][2][0]] = " "
            self.squares[original[1]][original[0]] = " "
        else:
            self.squares[original[1]][original[0]] = " "
            self.squares[capture[1]][capture[0]] = " "

    def check_win(self):
        
        return