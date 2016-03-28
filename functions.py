#  Jianyu Zheng 33062456.  ICS 32 Lab sec 5.  Lab asst 4.


import launcher
import tkinter



background_color = '#99FF99'
line_color = 'black'
black_piece = 'black'
white_piece = 'white'

class GameOverError(BaseException):
    '''Raised when game is over'''
    pass

class InvalidMoveError(BaseException):
    '''Raised when an invalid move is made'''
    pass

class NoLegalMoveError(BaseException):
    '''Raised when the player has no legal place to drop piece'''
    pass

class board:
    '''collection of functions about Reversi game'''
    def __init__(self, launcher: launcher.Launcher):
        result = []
        self._launcher = launcher
        options = self._launcher.start()
        self._board_rows = options[0]
        self._board_columns = options[1]
        turn = turn_determine(options[2])
        self._turn = turn
##        print(self._turn)
        self._topleft = color_determine(options[3])
        self._victory = options[4]
        self._NONE = '*'
        self._WHITE = 'W'
        self._BLACK = 'B'
        board = create_board(self._board_rows, self._board_columns, self._NONE)
        self._board = center_cells(board, self._topleft, self._board_rows, self._board_columns)
        self._blackpiece = count_pieces(self._board, self._BLACK)
        self._whitepiece = count_pieces(self._board, self._WHITE)


    def print_board(self):
        print("It's {} player's turn.      Black piece:{}      White piece:{}".format\
              (full_name(self._turn), count_pieces(self._board, self._BLACK), count_pieces(self._board, self._WHITE)))
        print('--------------------------------------------------------------')
        for a in self._board:
            for b in range(len(a) + 1):
                print('{:<2d}'.format(b), end=' ')
            print()
            break
        for c in range(len(self._board)):
            print('{:<2d}'.format(c + 1), end = ' ')
            for d in self._board[c]:
                print(d, end = '  ')
            print()
        print()

    def make_move(self, row: int, column: int):
        self._board = drop_piece(self._board, row, column, self._turn, self._NONE) 
        self._turn = change_turn(self._turn)



    def victory_condition(self):
##        print(count_pieces(self._board, self._BLACK))
##        print(count_pieces(self._board, self._WHITE))
##        print(self._board_rows * self._board_columns)
        if count_pieces(self._board, self._BLACK) == 0 or count_pieces(self._board, self._WHITE) == 0:
            raise GameOverError()
        elif count_pieces(self._board, self._BLACK) + count_pieces(self._board, self._WHITE) == self._board_rows * self._board_columns:
            raise GameOverError()
        else:
            pass


    def winner(self):
        if count_pieces(self._board, self._BLACK) > count_pieces(self._board, self._WHITE):
            return 'Black player wins!'
        elif count_pieces(self._board, self._BLACK) < count_pieces(self._board, self._WHITE):
            return 'White player wins!'
        else:
            return 'Draw.'

    def inverse_winner(self):
        if count_pieces(self._board, self._BLACK) > count_pieces(self._board, self._WHITE):
            return 'White player wins!'
        elif count_pieces(self._board, self._BLACK) < count_pieces(self._board, self._WHITE):
            return 'Black player wins!'
        else:
            return 'Draw.'

    def check_move(self):
        count = 0
        copy_board = copy_game_board(self._board, self._board_rows, self._board_columns)
        for a in range(len(copy_board)):
            for b in range(len(copy_board[a])):
                if copy_board[a][b] == self._NONE:
                    count += check_board(copy_board, a, b, self._turn)
                else:
                    count += 8
##        print(count)
##        print(self._board_rows * self._board_columns * 8)
##        print(count < self._board_rows * self._board_columns * 8)
        if count < self._board_rows * self._board_columns * 8:
            pass
        else:
            self._turn = change_turn(self._turn)
##            print(self._board)
##            print('here')
            raise NoLegalMoveError()

    def total(self):
        copy_board = copy_game_board(self._board, self._board_rows, self._board_columns)
        total_pieces = count_pieces(copy_board, self._BLACK) + count_pieces(copy_board, self._WHITE)
        return total_pieces


    def double_illegal(self):
        count = 0
        copy_board = copy_game_board(self._board, self._board_rows, self._board_columns)
        for a in range(len(copy_board)):
            for b in range(len(copy_board[a])):
                if copy_board[a][b] == self._NONE:
                    count += check_board(copy_board, a, b, self._turn)
                else:
                    count += 8
        if count < self._board_rows * self._board_columns * 8:
            return True
        else:
            count1 = 0
            for a in range(len(copy_board)):
                for b in range(len(copy_board[a])):
                    if copy_board[a][b] == self._NONE:
##                        print(change_turn(self._turn))
                        count1 += check_board(copy_board, a, b, change_turn(self._turn))
                    else:
                        count1 += 8
            if count1 < self._board_rows * self._board_columns * 8:
                return True
            else:
                raise GameOverError()

                
            
def fix_variable(variable: list) -> list:
    result = []
    result.extend(variable)
    return result

def size_determine(sides: int) -> int:
    '''takes an integer and returns if it is even and between 4 and 16'''
    try:
        if not 4 <= int(sides) <= 16:
            sides = int(input('Invalid length. The side length of the chessboard should be between 4 and 16.\nPlease try again: '))
            return size_determine(sides)
        elif int(sides) % 2 != 0:
            sides = int(input('Invalid number. The side length should be even.\nPlease try again: '))
            return size_determine(sides)
        else:
            print()
            return int(sides)
    except:
        sides = int(input('Invalid value. Please try again: '))
        return size_determine(sides)

def turn_determine(turn: str) -> str:
    '''takes a string and returns if it is W, or B'''
    try:
        if turn == 'White Player':
            print()
            return 'W'
        elif turn == 'Black Player':
            print()
            return 'B'
        else:
            new_turn = input('Error. "' + turn + '" is not a valid command.\nPlease try again: ')
            return turn_determine(new_turn)
    except:
        new_turn = input('Error. "' + turn + '" is not a valid command.\nPlease try again: ')
        return turn_determine(new_turn)

def color_determine(color: str) -> str:
    '''takes a color and returns the abbr of it'''
    if color == 'White':
        return 'W'
    else:
        return 'B'

##def vectory_condition_determine(condition: str) -> str:
##    '''takes a string and returns if it is A, or B'''
##    try:
##        if condition.upper() == 'A':
##            print()
##            return 'A'
##        elif condition.upper() == 'B':
##            print()
##            return 'B'
##        else:
##            conditions = input('Error. "' + condition + '" is not a valid command.\nPlease try again: ')
##            return vectory_condition_determine(conditions)
##    except:
##        conditions = input('Error. "' + condition + '" is not a valid command.\nPlease try again: ')
##        return vectory_condition_determine(conditions)

def create_board(rows: int, columns: int, piece: str) -> list:
    '''takes the size of the board, and returns the list of it'''
    result = []
    for a in range(rows):
        result.append([])
        for b in range(columns):
            result[-1].append(piece)
    return result

def copy_game_board(board: list, rows: int, columns: int) -> list:
    '''Copies the given game board'''
    result = []
    for a in range(rows):
        result.append([])
        for b in range(columns):
            result[-1].append(board[a][b])
    return result

def center_cells(board: list, top_left: str, rows: int, columns: int) -> list:
    '''takes a board list, a top-left piece color, and the size of board, returns a board with filled center cells'''
    if top_left == 'W':
        board[int(rows/2 - 1)][int(columns/2 - 1)] = 'W'
        board[int(rows/2)][int(columns/2)] = 'W'
        board[int(rows/2)][int(columns/2 - 1)] = 'B'
        board[int(rows/2 - 1)][int(columns/2)] = 'B'
        return board
    else:
        board[int(rows/2 - 1)][int(columns/2 - 1)] = 'B'
        board[int(rows/2)][int(columns/2)] = 'B'
        board[int(rows/2)][int(columns/2 - 1)] = 'W'
        board[int(rows/2 - 1)][int(columns/2)] = 'W'
        return board

def full_name(color: str) -> str:
    '''takes a 'W' or 'B', returns its full name'''
    if color == 'W':
        return 'white'
    else:
        return 'black'
        
def change_turn(turn: str) -> str:
    '''takes a string of turn color and returns another color'''
    if turn == 'W':
        return 'B'
    else:
        return 'W'

def count_pieces(board: list, color: str) -> int:
    '''takes a board list and a color string, returns the pieces of the player'''
    count = 0
    for a in board:
        for b in a:
            if b == color:
                count += 1
    return count

def drop_piece(board: list, row: int, column: int, turn: str, none: str) -> list:
    '''takes a list, a coordinate and the turn, returns a changed board'''
    if board[row - 1][column - 1] == none:
        newboard = change_board(board, row-1, column-1, turn)
        return newboard
    else:
        raise InvalidMoveError()

                
def change_board(board: list, row: int, column: int, turn: str) -> bool:
    '''takes a move, returns whether it is valid'''
    result = 0
    try:
        if board[row+1][column] == change_turn(turn):
            i = 2
            while True:
                if board[row+i][column] == change_turn(turn):
                    i += 1
                elif board[row+i][column] == turn:
                    for x in range(i):
                        board[row+x][column] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row-1][column] == change_turn(turn):
            i = 2
            if row - i < 0:
                raise IndexError
            while True:
                if board[row-i][column] == change_turn(turn):
                    i += 1
                elif board[row-i][column] == turn:
                    for x in range(i):
                        board[row-x][column] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row][column+1] == change_turn(turn):
            i = 2
            while True:
                if board[row][column+i] == change_turn(turn):
                    i += 1
                elif board[row][column+i] == turn:
                    for x in range(i):
                        board[row][column+x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row][column-1] == change_turn(turn):
            i = 2
            if column - i < 0:
                raise IndexError
            while True:
                if board[row][column-i] == change_turn(turn):
                    i += 1
                elif board[row][column-i] == turn:
                    for x in range(i):
                        board[row][column-x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row+1][column+1] == change_turn(turn):
            i = 2
            while True:
                if board[row+i][column+i] == change_turn(turn):
                    i += 1
                elif board[row+i][column+i] == turn:
                    for x in range(i):
                        board[row+x][column+x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row+1][column-1] == change_turn(turn):
            i = 2
            if column - i < 0:
                raise IndexError
            while True:
                if board[row+i][column-i] == change_turn(turn):
                    i += 1
                elif board[row+i][column-i] == turn:
                    for x in range(i):
                        board[row+x][column-x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row-1][column+1] == change_turn(turn):
            i = 2
            if row - i < 0:
                raise IndexError
            while True:
                if board[row-i][column+i] == change_turn(turn):
                    i += 1
                elif board[row-i][column+i] == turn:
                    for x in range(i):
                        board[row-x][column+x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row-1][column-1] == change_turn(turn):
            i = 2
            if row - i < 0:
                raise IndexError
            if column - i < 0:
                raise IndexError
            while True:
                if board[row-i][column-i] == change_turn(turn):
                    i += 1
                elif board[row-i][column-i] == turn:
                    for x in range(i):
                        board[row-x][column-x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    if result >= 8:
        raise InvalidMoveError()
    return board


def check_board(board: list, row: int, column: int, turn: str) -> bool:
    '''takes a move, returns whether it is valid'''
    result = 0
    try:
        if board[row+1][column] == change_turn(turn):
            i = 2
            while True:
                if board[row+i][column] == change_turn(turn):
##                    print('yeah')
                    i += 1
                elif board[row+i][column] == turn:
##                    print('!!!')
                    pass
##                    for x in range(i):
##                        board[row+x][column] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row-1][column] == change_turn(turn):
            i = 2
            if row - i < 0:
                raise IndexError
            while True:
                if board[row-i][column] == change_turn(turn):
                    i += 1
                elif board[row-i][column] == turn:
                    pass
##                    for x in range(i):
##                        board[row-x][column] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row][column+1] == change_turn(turn):
            i = 2
            while True:
                if board[row][column+i] == change_turn(turn):
                    i += 1
                elif board[row][column+i] == turn:
                    pass
##                    for x in range(i):
##                        board[row][column+x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row][column-1] == change_turn(turn):
            i = 2
            if column - i < 0:
                raise IndexError
            while True:
                if board[row][column-i] == change_turn(turn):
                    i += 1
                elif board[row][column-i] == turn:
                    pass
##                    for x in range(i):
##                        board[row][column-x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row+1][column+1] == change_turn(turn):
            i = 2
            while True:
                if board[row+i][column+i] == change_turn(turn):
                    i += 1
                elif board[row+i][column+i] == turn:
                    pass
##                    for x in range(i):
##                        board[row+x][column+x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row+1][column-1] == change_turn(turn):
            i = 2
            if column - i < 0:
                raise IndexError
            while True:
                if board[row+i][column-i] == change_turn(turn):
                    i += 1
                elif board[row+i][column-i] == turn:
                    pass
##                    for x in range(i):
##                        board[row+x][column-x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row-1][column+1] == change_turn(turn):
            i = 2
            if row - i < 0:
                raise IndexError
            while True:
                if board[row-i][column+i] == change_turn(turn):
                    i += 1
                elif board[row-i][column+i] == turn:
                    pass
##                    for x in range(i):
##                        board[row-x][column+x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
    try:
        if board[row-1][column-1] == change_turn(turn):
            i = 2
            if row - i < 0:
                raise IndexError
            if column - i < 0:
                raise IndexError
            while True:
                if board[row-i][column-i] == change_turn(turn):
                    i += 1
                elif board[row-i][column-i] == turn:
                    pass
##                    for x in range(i):
##                        board[row-x][column-x] = turn
                    break
                else:
                    result += 1
                    break
        else:
            result += 1
    except IndexError:
        result += 1
##    print(result)
    return result





















