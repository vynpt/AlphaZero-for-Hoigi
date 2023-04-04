class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team ## -1 for black, 0 for empty square, 1 for white
        self.type = type
        ## pawn = 1
        ## king = 2
        ## fortress = 3
        ## spy = 4
        ## captain = 5
        ## cannon = 6
        ## musketeer = 7
        ## knight = 8
        ## samurai = 9
        ## archer = 10
        ## major = 11
        ## lieutenant = 12
        ## general = 13
        self.image = image
        self.value = 0
        self.onhold = True     ## if the piece is not on the board yet
        #self.killable = killable

    ## return the layers on a square in top to bottom order
    ##def get_layer(coordinate):
    ##    result = [x for x in board[coordinate[0]][coordinate[1]]]
    ##    return result[::-1]

    ## moves are in the form [team, type of piece, destination location, original position, capture]
    ## [self.team, self.type, [y,x,z], [y,x,z], boolean]

    ## methods for the movement of different pieces
    ## takes a board object, and the position of the piece
    ## return a list of valid moves excluding captures mechanics 

    def remove_invalid_moves(move_list):
        ## remove moves exceed boundaries of the board
        new_list = []
        for i in move_list:
            if ((i[2][0] >= 0) and (i[2][0] < 9) and (i[2][1] >= 0) and (i[2][1] < 9) and (i[2][2] >= 0) and (i[2][2] < 3)):
                new_list += [i]
        return new_list

    def pawn_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2): ## [layer3, layer2, layer1]
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0 and board[y - 1 * self.team ][x][i].type != "king"):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        else: ## pawn has same movements for layer2 and layer3
            num = 3
            ## check if the pawn is at left most side of the board, since negative array index will still be processed by try-except
            if (x - 1 >= 0): 
                x = x - 1
            else:
                num = 2
            for j in range(num):
                ## moves that are out of the board will be passed
                try:
                    if (board[y - 1 * self.team ][x + j][2] == " "):
                        result_moves += [self.team, self.type, [y - 1 * self.team, x + j, 2], position, False]
                    else:
                        for i in range(3): ## [layer3, layer2, layer1]
                            if (board[y - 1 * self.team ][x + j][i] == " "):
                                continue
                            elif (board[y - 1 * self.team ][x + j][i].team == self.team and i > 0 and board[y - 1 * self.team ][x + j][i].type != "king"):
                                result_moves += [self.team, self.type, [y - 1 * self.team, x + j, i-1], position, False]
                                break
                            elif (board[y - 1 * self.team ][x + j][i].team == -self.team):
                                result_moves += [self.team, self.type, [y - 1 * self.team, x + j, i], position, True]
                                break
                except:
                    pass
        
        return self.remove_invalid_moves(result_moves)
    
    def king_moves(self, board, position):
        ## cannot stack and be stacked on
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        ## account for negative out of bound on the board
        numj = 3
        numk = 3
        if (x - 1 >= 0): 
            x = x - 1
        else:
            numj = 2
        if (y - 1 >= 0): 
            y = y - 1
        else:
            numk = 2
        for j in range(numj):
            for k in range(numk):
                try:
                    if (j == position[1] and k == position[0]): ## check if the move is same as starting position
                        continue
                    if (board[y + k][x + j][2] == " "):
                        result_moves += [self.team, self.type, [y + k, x + j, 2], position, False]
                    if (board[y + k][x + j][0] == " " and board[y + k][x + j][1] == " " and board[y + k][x + j][2].team == -self.team):
                        result_moves += [self.team, self.type, [y + k, x + j, 2], position, True]                            
                except:
                    pass
        return self.remove_invalid_moves(result_moves)
    
    def fortress_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def spy_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def captain_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def cannon_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def musketeer_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def knight_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def samurai_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def archer_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def major_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def lieutenant_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)

    def general_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            try:
                if (board[y - 1 * self.team ][x][2] == " "):
                    result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
                            break
                        elif (board[y - 1 * self.team ][x][i].team == -self.team):
                            result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
                            break
            except:
                pass
        elif (z == 1):
            pass
        else:
            pass
        return self.remove_invalid_moves(result_moves)