class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team ## -1 for black, 0 for empty square, 1 for white
        self.image = image
        self.value = [1, 4, 5, 3, 3, 2, 4, 6, 7]
        self.onhold = True     ## if the piece is not on the board yet
        
        self.type = type
        ## empty = 0
        ## pawn = 1
        ## king = 2
        ## fortress = 3
        ## captain = 4
        ## cannon = 5
        ## musketeer = 6
        ## archer = 7
        ## lieutenant = 8
        ## general = 9

        ## spy = 10
        ## knight = 11
        ## samurai = 12
        ## major = 13

    ## return the layers on a square in top to bottom order
    ##def get_layer(coordinate):
    ##    result = [x for x in board[coordinate[0]][coordinate[1]]]
    ##    return result[::-1]

    ## moves are in the form [team, type of piece, destination location, original position, capture]
    ## [self.team, self.type, [y,x,z], [y,x,z], boolean]

    ## methods for the movement of different pieces
    ## takes a board object, and the position of the piece
    ## return a list of valid moves excluding captures mechanics 

    def __repr__(self):
        ## return a string letter representation of piece, capitalcase for white, lowercase black
        s = ""
        if (self.type == 1): # p = pawn
            s = "p"
        if (self.type == 2): # k = king
            s = "k"
        if (self.type == 3): # f = fortress
            s = "f"
        if (self.type == 4): # t = captain
            s = "t"
        if (self.type == 5): # c = cannon
            s = "c"
        if (self.type == 6): # m = musketeer
            s = "m"
        if (self.type == 7): # a = archer
            s = "a"
        if (self.type == 8): # l = lietenant
            s = "l"
        if (self.type == 9): # g = general
            s = "g"
        
        if (self.team == 1):  # capitalize strinng for white
            s = s.upper()
        return s

    def remove_invalid_moves(self, move_list):
        ## remove moves exceed boundaries of the board
        """
        new_list = []
        for i in move_list:
            if ((i[2][0] >= 0) and (i[2][0] < 9) and (i[2][1] >= 0) and (i[2][1] < 9) and (i[2][2] >= 0) and (i[2][2] < 3)):
                new_list += [i]
        return new_list
        """
        return move_list
    
    def pawn_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2): ## [layer3, layer2, layer1]
            # y > 0 and y < 8  is checking the edge of board
            # check
            if (y > 0 and y < 8 and board[y - (1 * self.team) ][x][2] == " "):
                result_moves.append([self.team, self.type, [y - 1 * self.team, x, 2], position, False])
            elif (y > 0 and y < 8 ):
                for i in range(3): ## [layer3, layer2, layer1]
                    if (board[y - 1 * self.team ][x][i] == " "):
                        continue
                    elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0 and board[y - 1 * self.team ][x][i].type != 2):
                        result_moves.append([self.team, self.type, [y - 1 * self.team, x, i-1], position, False])
                        break
                    elif (board[y - 1 * self.team ][x][i].team == -self.team):
                        result_moves.append([self.team, self.type, [y - 1 * self.team, x, i], position, True])
                        break
            
            
        else: ## pawn has same movements for layer2 and layer3
            num = 3
            ## check if the pawn is at left most side of the board, since negative array index will still be processed by try-except
            if (x - 1 >= 0): 
                x = x - 1
            else:
                num = 2
            for j in range(num):
                ## moves that are out of the board will be passed
                
                if (board[y - 1 * self.team ][x + j][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [y - 1 * self.team, x + j, 2], position, False])
                else:
                    for i in range(3): ## [layer3, layer2, layer1]
                        if (board[y - 1 * self.team ][x + j][i] == " "):
                            continue
                        elif (board[y - 1 * self.team ][x + j][i].team == self.team and i > 0 and board[y - 1 * self.team ][x + j][i].type != 2):
                            result_moves.append([self.team, self.type, [y - 1 * self.team, x + j, i-1], position, False])
                            break
                        elif (board[y - 1 * self.team ][x + j][i].team == -self.team):
                            result_moves.append([self.team, self.type, [y - 1 * self.team, x + j, i], position, True])
                            break
                
        
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
        if (x - 1 >= 0 and x + 1 <= 8): # check position not at edge
            x = x - 1
        elif(x - 1 < 0 and x + 1 <= 8): # check left edge
            numj = 2
        elif(x - 1 >= 0 and x + 1 > 8): # check right edge
            x = x - 1
            numj = 2

        if (y - 1 >= 0 and y + 1 <= 8): # check position not at edge
            y = y - 1
        elif(y - 1 < 0 and y + 1 <= 8): # check top edge
            numk = 2
        elif(y - 1 >= 0 and y + 1 > 8): # check bottom edge
            y = y - 1
            numk = 2
        
        for j in range(numj):
            for k in range(numk):
                if (x + j == position[1] and y + k == position[0]): ## check if the move is same as starting position
                    continue
                if (board[y + k][x + j][2] == " "):
                    result_moves.append([self.team, self.type, [y + k, x + j, 2], position, False])
                elif (board[y + k][x + j][0] == " " and board[y + k][x + j][1] == " " and board[y + k][x + j][2].team == -self.team):
                    result_moves.append([self.team, self.type, [y + k, x + j, 2], position, True])                          
        print("result_moves for king = ", result_moves)        
        return self.remove_invalid_moves(result_moves)
    
    def fortress_moves(self, board, position):
        ## cannot stack and cannot capture towers
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        ## account for negative out of bound on the board
        numj = 3
        numk = 3
        if (x - 1 >= 0 and x + 1 <= 8): # check position not at edge
            x = x - 1
        elif(x - 1 < 0 and x + 1 <= 8): # check left edge
            numj = 2
        elif(x - 1 >= 0 and x + 1 > 8): # check right edge
            x = x - 1
            numj = 2

        if (y - 1 >= 0 and y + 1 <= 8): # check position not at edge
            y = y - 1
        elif(y - 1 < 0 and y + 1 <= 8): # check top edge
            numk = 2
        elif(y - 1 >= 0 and y + 1 > 8): # check bottom edge
            y = y - 1
            numk = 2

        for j in range(numj):
            for k in range(numk):
                
                if (x + j == position[1] and y + k == position[0]): ## check if the move is same as starting position
                    continue
                if (board[y + k][x + j][2] == " "):
                    result_moves.append([self.team, self.type, [y + k, x + j, 2], position, False])
                elif (board[y + k][x + j][0] == " " and board[y + k][x + j][1] == " " and board[y + k][x + j][2].team == -self.team):
                    result_moves.append([self.team, self.type, [y + k, x + j, 2], position, True])                          
        return self.remove_invalid_moves(result_moves)

    def archer_moves(self, board, position):
        ## range based on tier
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]

        numj = 3 - z
        numk = 3 - z
        for k in range(-numk, numk + 1):
            if k == -numk or k == numk:
                j_list = range(-numj, numj + 1)
            else:
                j_list = [-numj, numj]
            
            for j in j_list:
                if (x + j == position[1] and y + k == position[0]): ## check if the move is same as starting position
                    continue
                if y+k < 0 or y+k > 7 or x+j < 0 or x+j > 7:  ## check out of bound
                    continue

                if (board[y + k][x + j][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [y + k][x + j][2], position, False])
                for l in range(3):
                    if (board[y + k][x + j][l] == " "):
                        continue
                    elif (board[y + k][x + j][l].team == self.team and l > 0 and board[y + k][x + j][l].type != 2):
                        result_moves.append([self.team, self.type, [y+k, x+j, l-1], position, False])
                        break
                    elif (board[y + k][x + j][l].team == -self.team):
                        result_moves.append([self.team, self.type, [y+k, x+j, l], position, True])
                        break 

        return self.remove_invalid_moves(result_moves)

    def lieutenant_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]

        if (z == 2):
            possible = [[y-1, x-1], [y-1, x], [y - 1 * self.team, x+1], [y+1, x-1], [y+1, x+1]]
            for i in range(len(possible)):
                if possible[i][0] < 0 or possible[i][0] > 7 or possible[i][1] < 0 or possible[i][1] > 7:
                    continue
                if (board[possible[i][0]][possible[i][1]][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [possible[i][0]][possible[i][1]][2], position, False])
                for l in range(3):
                    if (board[possible[i][0]][possible[i][1]][l] == " "):
                        continue
                    elif (board[possible[i][0]][possible[i][1]][l].team == self.team and l > 0 and board[possible[i][0]][possible[i][1]][l].type != 2):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l-1], position, False])
                        break
                    elif (board[possible[i][0]][possible[i][1]][l].team == -self.team):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l], position, True])
                        break
        if (z == 1):
            possible = [[y-1, x-1], [y-1, x], [y-1, x+1], [y+1, x-1], [y+1, x], [y+1, x+1]]
            for i in range(len(possible)):
                if possible[i][0] < 0 or possible[i][0] > 7 or possible[i][1] < 0 or possible[i][1] > 7:
                    continue
                if (board[possible[i][0]][possible[i][1]][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [possible[i][0]][possible[i][1]][2], position, False])
                for l in range(3):
                    if (board[possible[i][0]][possible[i][1]][l] == " "):
                        continue
                    elif (board[possible[i][0]][possible[i][1]][l].team == self.team and l > 0 and board[possible[i][0]][possible[i][1]][l].type != 2):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l-1], position, False])
                        break
                    elif (board[possible[i][0]][possible[i][1]][l].team == -self.team):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l], position, True])
                        break 
        if (z == 0):
            possible = [[y-1, x-1], [y-1, x], [y-1, x+1], [y+1, x-1], [y+1, x], [y+1, x+1], [y, x-1], [y, x+1]]
            for i in range(len(possible)):
                if possible[i][0] < 0 or possible[i][0] > 7 or possible[i][1] < 0 or possible[i][1] > 7:
                    continue
                if (board[possible[i][0]][possible[i][1]][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [possible[i][0]][possible[i][1]][2], position, False])
                for l in range(3):
                    if (board[possible[i][0]][possible[i][1]][l] == " "):
                        continue
                    elif (board[possible[i][0]][possible[i][1]][l].team == self.team and l > 0 and board[possible[i][0]][possible[i][1]][l].type != 2):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l-1], position, False])
                        break
                    elif (board[possible[i][0]][possible[i][1]][l].team == -self.team):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l], position, True])
                        break  
        print("result moves for lieutenant: ", result_moves)                     
        return self.remove_invalid_moves(result_moves)

    def general_moves(self, board, position):
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]
        if (z == 2):
            possible = [[y - 1 * self.team, x-1], [y-1, x], [y - 1 * self.team, x+1], [y, x-1], [y, x+1], [y+1, x]]
            for i in range(len(possible)):
                if possible[i][0] < 0 or possible[i][0] > 7 or possible[i][1] < 0 or possible[i][1] > 7:
                    continue
                if (board[possible[i][0]][possible[i][1]][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [possible[i][0]][possible[i][1]][2], position, False])
                for l in range(3):
                    if (board[possible[i][0]][possible[i][1]][l] == " "):
                        continue
                    elif (board[possible[i][0]][possible[i][1]][l].team == self.team and l > 0 and board[possible[i][0]][possible[i][1]][l].type != 2):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l-1], position, False])
                        break
                    elif (board[possible[i][0]][possible[i][1]][l].team == -self.team):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l], position, True])
                        break
        if (z == 1):
            possible = [[y-1, x-1], [y-1, x], [y-1, x+1], [y+1, x-1], [y+1, x], [y+1, x+1], [y, x-1], [y, x+1]]
            for i in range(len(possible)):
                if possible[i][0] < 0 or possible[i][0] > 7 or possible[i][1] < 0 or possible[i][1] > 7:
                    continue
                if (board[possible[i][0]][possible[i][1]][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [possible[i][0]][possible[i][1]][2], position, False])
                for l in range(3):
                    if (board[possible[i][0]][possible[i][1]][l] == " "):
                        continue
                    elif (board[possible[i][0]][possible[i][1]][l].team == self.team and l > 0 and board[possible[i][0]][possible[i][1]][l].type != 2):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l-1], position, False])
                        break
                    elif (board[possible[i][0]][possible[i][1]][l].team == -self.team):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l], position, True])
                        break 
        if (z == 0):
            possible = [[y-1, x-1], [y-1, x], [y-1, x+1], [y+1, x-1], [y+1, x], [y+1, x+1], [y, x-1], [y, x+1], [y - 2 * self.team, x-1], [y - 2 * self.team, x], [y - 2 * self.team, x+1]]
            for i in range(len(possible)):
                if possible[i][0] < 0 or possible[i][0] > 7 or possible[i][1] < 0 or possible[i][1] > 7:
                    continue
                if (board[possible[i][0]][possible[i][1]][2] == " "):  # the empty square is a possible move
                        result_moves.append([self.team, self.type, [possible[i][0]][possible[i][1]][2], position, False])
                for l in range(3):
                    if (board[possible[i][0]][possible[i][1]][l] == " "):
                        continue
                    elif (board[possible[i][0]][possible[i][1]][l].team == self.team and l > 0 and board[possible[i][0]][possible[i][1]][l].type != 2):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l-1], position, False])
                        break
                    elif (board[possible[i][0]][possible[i][1]][l].team == -self.team):
                        result_moves.append([self.team, self.type, [possible[i][0], possible[i][1], l], position, True])
                        break                       
        return self.remove_invalid_moves(result_moves)

    def captain_moves(self, board, position):
        ## tier 1: move 1-square, tier 2 & 3: capture movement of the piece below
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]

        if (z == 2):   ## [layer3, layer2, layer1]
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
                        if (x + j == position[1] and y + k == position[0]): ## check if the move is same as starting position
                            continue

                        if (board[y + k][x + j][2] == " "):  # the empty square is a possible move
                            result_moves.append([self.team, self.type, [y + k][x + j][2], position, False])
                        for l in range(3):
                            if (board[y + k][x + j][l] == " "):
                                continue
                            elif (board[y + k][x + j][l].team == self.team and l > 0 and board[y + k][x + j][l].type != 2):
                                result_moves.append([self.team, self.type, [y + k, x + j, l - 1], position, False])
                                break
                            elif (board[y + k][x + j][l].team == -self.team):
                                result_moves.append([self.team, self.type, [y + k, x + j, l], position, True])
                                break                           
                    except:
                        pass
        else:  ## captain is similar for layer2 and layer3         
#            print("[y][x][z+1] = ", board[y][x][z+1])
            result_moves = board[y][x][z+1].moves(board, [y,x,z+1])
        return self.remove_invalid_moves(result_moves)

    def cannon_moves(self, board, position):
        ## move orthogonally
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]

        move = 3 - z   ## move i-square orthogonally
        for i in range(-move, move + 1):
            if (i == 0):
                continue
            if (y+i >= 0 and y+i < 8):    ## check out of bound
                if (board[y+i][x][2] == " "):  # the empty square is a possible move
                    result_moves.append([self.team, self.type, [y+i][x][2], position, False])
                for ly in range(3):
                    if (board[y+i][x][ly] == " "):
                        continue
                    elif (board[y+i][x][ly].team == self.team and ly > 0 and board[y+i][x][ly].type != 2):
                        result_moves.append([self.team, self.type, [y+i, x, ly-1], position, False])
                        break
                    elif (board[y+i][x][ly].team == -self.team):
                        result_moves.append([self.team, self.type, [y+i, x, ly], position, True])
                        break 
            
            if (x+i >= 0 and x+i < 8):    ## check out of bound
                if (board[y][x+i][2] == " "):  # the empty square is a possible move
                    result_moves.append([self.team, self.type, [y][x + i][2], position, False])        
                for lx in range(3):
                    if (board[y][x+i][lx] == " "):
                        continue
                    elif (board[y][x+i][lx].team == self.team and lx > 0 and board[y][x+i][lx].type != 2):
                        result_moves.append([self.team, self.type, [y, x+i, lx-1], position, False])
                        break
                    elif (board[y][x+i][lx].team == -self.team):
                        result_moves.append([self.team, self.type, [y, x+i, lx], position, True])
                        break 
        return self.remove_invalid_moves(result_moves)

    def musketeer_moves(self, board, position):
        ## move straight forward based on tier
        result_moves = []     ## list of possible moves
        y = position[0]
        x = position[1]
        z = position[2]

        move = 3 - z   ## move i-square orthogonally
        for i in range(1, move + 1):
            if (y - i * self.team >= 0 and y - i * self.team < 8):    ## check out of bound
                if (board[y - i * self.team][x][2] == " "):  # the empty square is a possible move
                    result_moves.append([self.team, self.type, [y - i * self.team][x][2], position, False]) 
                for l in range(3):
                    if (board[y - i * self.team][x][l] == " "):
                        continue
                    elif (board[y - i * self.team][x][l].team == self.team and l > 0 and board[y - i * self.team][x][l].type != 2):
                        result_moves.append([self.team, self.type, [y - i * self.team, x, l-1], position, False])
                        break
                    elif (board[y - i * self.team][x][l].team == -self.team):
                        result_moves.append([self.team, self.type, [y - i * self.team, x, l], position, True])
                        break 
        return self.remove_invalid_moves(result_moves)

    def moves(self, board, position):
        # generate a list of moves for the current piece object
        movelist = []
        if (self.type == 1):
            
            movelist = self.pawn_moves(board, position) 
        if (self.type == 2):
            movelist = self.king_moves(board, position)
        if (self.type == 3):
            movelist = self.fortress_moves(board, position)
        if (self.type == 4):
            movelist = self.archer_moves(board, position)
        if (self.type == 5):
            movelist = self.lieutenant_moves(board, position)
        if (self.type == 6):
            movelist = self.general_moves(board, position)
        if (self.type == 7):
            movelist = self.captain_moves(board, position)
        if (self.type == 8):
            movelist = self.cannon_moves(board, position)
        if (self.type == 9):
            movelist = self.musketeer_moves(board, position)
        
        #print("move list of this type ", self.type, " is ", movelist)
        return movelist



# code we are not using

    # def knight_moves(self, board, position):
    #     result_moves = []     ## list of possible moves
    #     y = position[0]
    #     x = position[1]
    #     z = position[2]
    #     if (z == 2):
    #         try:
    #             if (board[y - 1 * self.team ][x][2] == " "):
    #                 result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
    #             else:
    #                 for i in range(3): ## [layer3, layer2, layer1]
    #                     if (board[y - 1 * self.team ][x][i] == " "):
    #                         continue
    #                     elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
    #                         break
    #                     elif (board[y - 1 * self.team ][x][i].team == -self.team):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
    #                         break
    #         except:
    #             pass
    #     elif (z == 1):
    #         pass
    #     else:
    #         pass
    #     return self.remove_invalid_moves(result_moves)

    # def samurai_moves(self, board, position):
    #     result_moves = []     ## list of possible moves
    #     y = position[0]
    #     x = position[1]
    #     z = position[2]
    #     if (z == 2):
    #         try:
    #             if (board[y - 1 * self.team ][x][2] == " "):
    #                 result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
    #             else:
    #                 for i in range(3): ## [layer3, layer2, layer1]
    #                     if (board[y - 1 * self.team ][x][i] == " "):
    #                         continue
    #                     elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
    #                         break
    #                     elif (board[y - 1 * self.team ][x][i].team == -self.team):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
    #                         break
    #         except:
    #             pass
    #     elif (z == 1):
    #         pass
    #     else:
    #         pass
    #     return self.remove_invalid_moves(result_moves)

    # def major_moves(self, board, position):
    #     result_moves = []     ## list of possible moves
    #     y = position[0]
    #     x = position[1]
    #     z = position[2]
    #     if (z == 2):
    #         try:
    #             if (board[y - 1 * self.team ][x][2] == " "):
    #                 result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
    #             else:
    #                 for i in range(3): ## [layer3, layer2, layer1]
    #                     if (board[y - 1 * self.team ][x][i] == " "):
    #                         continue
    #                     elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
    #                         break
    #                     elif (board[y - 1 * self.team ][x][i].team == -self.team):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
    #                         break
    #         except:
    #             pass
    #     elif (z == 1):
    #         pass
    #     else:
    #         pass
    #     return self.remove_invalid_moves(result_moves)
        # def spy_moves(self, board, position):
    #     result_moves = []     ## list of possible moves
    #     y = position[0]
    #     x = position[1]
    #     z = position[2]
    #     if (z == 2):
    #         try:
    #             if (board[y - 1 * self.team ][x][2] == " "):
    #                 result_moves += [self.team, self.type, [y - 1 * self.team, x, 2], position, False]
    #             else:
    #                 for i in range(3): ## [layer3, layer2, layer1]
    #                     if (board[y - 1 * self.team ][x][i] == " "):
    #                         continue
    #                     elif (board[y - 1 * self.team ][x][i].team == self.team and i > 0):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i-1], position, False]
    #                         break
    #                     elif (board[y - 1 * self.team ][x][i].team == -self.team):
    #                         result_moves += [self.team, self.type, [y - 1 * self.team, x, i], position, True]
    #                         break
    #         except:
    #             pass
    #     elif (z == 1):
    #         pass
    #     else:
    #         pass
    #     return self.remove_invalid_moves(result_moves)
