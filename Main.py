
from Letter import*
from Symbol import*
from Hoigi_Pieces import*
from Hoigi_Board import*
import pygame
import time
import sys

def load_images():
    b_pawn = Piece(-1, 'pawn', 'Letter/b_pawn.png')
    w_pawn = Piece(1, 'pawn', 'Letter/w_pawn.png')
    b_king = Piece(-1, 'king', 'Letter/b_king.png')
    w_king = Piece(1, 'king', 'Letter/w_king.png')
    b_fortress = Piece(-1, 'fortress', 'Letter/b_fortress.png')
    w_fortress = Piece(1, 'fortress', 'Letter/w_fortress.png')
    b_spy = Piece(-1, 'spy', 'Letter/b_spy.png')
    w_spy = Piece(1, 'spy', 'Letter/w_spy.png')
    b_captain = Piece(-1, 'captain', 'Letter/b_captain.png')
    w_captain = Piece(1, 'captain', 'Letter/w_captain.png')
    b_cannon = Piece(-1, 'cannon', 'Letter/b_cannon.png')
    w_cannon = Piece(1, 'cannon', 'Letter/w_cannon.png')
    b_musketeer = Piece(-1, 'musketeer', 'Letter/b_musketeer.png')
    w_musketeer = Piece(1, 'musketeer', 'Letter/w_musketeer.png')
    b_knight = Piece(-1, 'knight', 'Letter/b_knight.png')
    w_knight = Piece(1, 'knight', 'Letter/w_knight.png')
    b_samurai = Piece(-1, 'samurai', 'Letter/b_samurai.png')
    w_samurai = Piece(1, 'samurai', 'Letter/w_samurai.png')
    b_archer = Piece(-1, 'archer', 'Letter/b_archer.png')
    w_archer = Piece(1, 'archer', 'Letter/w_archer.png')
    b_major = Piece(-1, 'major', 'Letter/b_major.png')
    w_major = Piece(1, 'major', 'Letter/w_major.png')
    b_lieutenant = Piece(-1, 'lieutenant', 'Letter/b_lieutenant.png')
    w_lieutenant = Piece(1, 'lieutenant', 'Letter/w_lieutenant.png')
    b_general = Piece(-1, 'general', 'Letter/b_general.png')
    w_general = Piece(1, 'general', 'Letter/w_general.png')
    pygame.image.load(b_pawn.image)
    pygame.image.load(w_pawn.image)
    pygame.image.load(b_king.image)
    pygame.image.load(w_king.image)
    pygame.image.load(b_fortress.image)
    pygame.image.load(w_fortress.image)
    pygame.image.load(b_spy.image)
    pygame.image.load(w_spy.image)
    pygame.image.load(b_captain.image)
    pygame.image.load(w_captain.image)
    pygame.image.load(b_cannon.image)
    pygame.image.load(w_cannon.image)
    pygame.image.load(b_musketeer.image)
    pygame.image.load(w_musketeer.image)
    pygame.image.load(b_knight.image)
    pygame.image.load(w_knight.image)
    pygame.image.load(b_samurai.image)
    pygame.image.load(w_samurai.image)
    pygame.image.load(b_archer.image)
    pygame.image.load(w_archer.image)
    pygame.image.load(b_major.image)
    pygame.image.load(w_major.image)
    pygame.image.load(b_lieutenant.image)
    pygame.image.load(w_lieutenant.image)
    pygame.image.load(b_general.image)
    pygame.image.load(w_general.image)

WIDTH = 720 ## size of board drawn

WIN = pygame.display.set_mode((WIDTH, WIDTH))

""" This is creating the window that we are playing on, it takes a tuple argument which is the dimensions of the window so in this case 900 x 900px
"""

pygame.display.set_caption("Hoigi")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 9, WIDTH / 9))

    def setup(self, WIN):
        b_pawn = Piece(-1, 'pawn', 'Letter/b_pawn.png')
        WIN.blit(pygame.image.load(b_pawn.image), (self.x, self.y))
        pass
        
def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
    return grid
"""
This is creating the nodes thats are on the board(so the Hoigi tiles)
I've put them into a 2d array which is identical to the dimesions of the board
"""


def draw_grid(win, rows, width):
    gap = width // 9
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

    """
    The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
    from each other and that is what this function does"""


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def Find_Node(pos, WIDTH):
    interval = WIDTH / 9
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE
        """
        Displays all the potential moves
        """

'''
def Do_Move(OriginalPos, FinalPosition, WIN):
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None
'''

def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid
"""this takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the node it is moving to
you can get those co-ordinates using my old function for swap"""

##create_board(board)


def main(WIN, WIDTH):
    load_images()
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(9, WIDTH)
    while True:
        pygame.time.delay(50) ##stops cpu dying
        for event in pygame.event.get():
            #WIN.blit(pygame.image.load(b_pawn.image), )
           
            update_display(WIN, grid, 9, WIDTH)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            """This quits the program if the player closes the window"""
'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                if selected == False:
                    try:
                        possible = select_moves((board[x][y]), (x,y), moves)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x,y
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')
                    #print(piece_to_move)

                else:
                    try:
                        if board[x][y].killable == True:
                            row, col = piece_to_move ## coords of original piece
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            Do_Move((col, row), (y, x), WIN)
                            moves += 1
                            print(convert_to_readable(board))
                        else:
                            deselect()
                            remove_highlight(grid)
                            selected = False
                            print("Deselected")
                    except:
                        if board[x][y] == 'x ':
                            row, col = piece_to_move
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            Do_Move((col, row), (y, x), WIN)
                            moves += 1
                            print(convert_to_readable(board))
                        else:
                            deselect()
                            remove_highlight(grid)
                            selected = False
                            print("Invalid move")
                    selected = False

            update_display(WIN, grid, 9, WIDTH)
'''

'''
def main():     # main program for running the chess game
    b1 = board(9,9,3)
    p1 = Player(0)
    p2 = Random_player(1)
    
    print(b1)
    # check if the entered move is valid


    while True:

        if process_move(b1, p1, p2) == True:
            return b1
        # making a random move
        if process_move(b1, p2, p1) == True:
            return b1
'''

main(WIN, WIDTH)
