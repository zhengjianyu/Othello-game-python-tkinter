#  Jianyu Zheng 33062456.  ICS 32 Lab sec 5.  Lab asst 5.


import launcher
import functions as F
import tkinter


DEFAULT_FONT = ('Helvetica', 14)
background_color = '#99FF99'
line_color = 'black'
black_piece = 'black'
white_piece = 'white'
font_color = 'black'

class OthelloGame:
    '''collection of functions about Reversi game'''
    def __init__(self, launcher: launcher.Launcher):
        self._launcher = launcher
        game = F.board(self._launcher)
        self._state = game
        self._board = self._state._board
        self._turn = self._state._turn
        options = self._launcher.start()
        self._rows = options[0]
        self._columns = options[1]
        self._move_first = options[2]
        self._topleft = options[3]
        self._victory_condition = options[4]
        
        self._game_window = tkinter.Tk()
        self._game_window.title('Othello')
        self._canvas = tkinter.Canvas(master = self._game_window, width = (self._columns + 2) * 50, height = (self._rows + 2) * 50, background = background_color)
        self._canvas.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = 'wesn')
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._scoreboard = tkinter.Canvas(master = self._game_window, width = 150, height = self._rows * 50 + 100, background = background_color)
        self._scoreboard.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = 'wesn')
        self._scoreboard.bind('<Configure>', self._on_scoreboard_resized)
        self._game_window.rowconfigure(0, weight = 1)
        self._game_window.columnconfigure(0, weight = int((self._columns + 2) * 50 / 150))
        self._game_window.columnconfigure(1, weight = 1)
        self._canvas.bind('<Button-1>', self._on_mouse_pressed)
        self._canvas.bind('<ButtonRelease-1>', self._drop_piece)
        self._canvas.bind('<Motion>', self._on_mouse_moved)
        self._highlighter_exist = False

        

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        self._redraw_mainboard()

    def _redraw_mainboard(self) -> None:
        self._canvas.delete(tkinter.ALL)
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()
        self._onerow_length = self._canvas_height / (self._rows + 2)
        self._onecolumn_length = self._canvas_width / (self._columns + 2)
        for i in range(self._rows + 1):
            self._canvas.create_line(self._onecolumn_length,
                                     (i + 1) * self._onerow_length,
                                     self._canvas_width - self._onecolumn_length,
                                     (i + 1) * self._onerow_length,
                                     fill = line_color)
        for i in range(self._columns + 1):
            self._canvas.create_line((i + 1) * self._onecolumn_length,
                                     self._onerow_length,
                                     (i + 1) * self._onecolumn_length,
                                     self._canvas_height - self._onerow_length,
                                     fill = line_color)

        self._coordinates = []
        for i in range(self._rows):
            self._coordinates.append([])
            for n in range(self._columns):
                self._coordinates[i].append([])
                for c in range(4):
                    self._coordinates[i][n].append(0)
        for i in range(self._rows):
            for n in range(self._columns):
                self._coordinates[i][n][0] = (n + 1) * self._onecolumn_length
                self._coordinates[i][n][1] = (i + 1) * self._onerow_length
                self._coordinates[i][n][2] = (n + 2) * self._onecolumn_length
                self._coordinates[i][n][3] = (i + 2) * self._onerow_length

        self._pieces = self._coordinates # change the size of piece
        for i in range(self._rows):
            for n in range(self._columns):
                self._pieces[i][n][0] += self._onecolumn_length * 0.1
                self._pieces[i][n][1] += self._onerow_length * 0.1
                self._pieces[i][n][2] -= self._onecolumn_length * 0.1
                self._pieces[i][n][3] -= self._onerow_length * 0.1
        for i in range(len(self._board)):
            for n in range(len(self._board[0])):
                if self._board[i][n] == 'B':
                    self._draw_piece('B',i,n)
                elif self._board[i][n] == 'W':
                    self._draw_piece('W',i,n)

    def _draw_piece(self, color: str, row: int, column: int):
        if color == 'B':
            self._canvas.create_oval(self._pieces[row][column][0],
                                    self._pieces[row][column][1],
                                    self._pieces[row][column][2],
                                    self._pieces[row][column][3],
                                    outline = black_piece,
                                    fill = black_piece)
        if color == 'W':
            self._canvas.create_oval(self._pieces[row][column][0],
                                    self._pieces[row][column][1],
                                    self._pieces[row][column][2],
                                    self._pieces[row][column][3],
                                    outline = white_piece,
                                    fill = white_piece)
                                 
    def _on_scoreboard_resized(self, event: tkinter.Event) -> None:
        self._redraw_scoreboard()

    def _redraw_scoreboard(self):
        self._scoreboard.delete(tkinter.ALL)
        self._scoreboardwidth = self._scoreboard.winfo_width()
        self._scoreboardheight = self._scoreboard.winfo_height()
        self.circlelength = self._scoreboardheight / (self._rows + 2)* 0.7
        self._black = F.count_pieces(self._board, 'B')
        self._white = F.count_pieces(self._board, 'W')
        self._massage_box = ''
        self._scoreboard.create_rectangle(self._scoreboardwidth * 0.15,
                                          self._scoreboardheight * 0.1,
                                          self._scoreboardwidth * 0.85,
                                          self._scoreboardheight * 0.6,
                                          outline = line_color)
        self._scoreboard.create_text(self._scoreboardwidth * 0.3,
                                     self._scoreboardheight * 0.2,
                                     font = DEFAULT_FONT,
                                     text = 'Turn:',
                                     fill = font_color)
        if self._turn == 'B':
            self._scoreboard.create_oval(self._scoreboardwidth * 0.5,
                                         self._scoreboardheight * 0.17,
                                         self._scoreboardwidth * 0.5 + self.circlelength,
                                         self._scoreboardheight * 0.17 + self.circlelength,
                                         outline = black_piece,
                                         fill = black_piece)
        elif self._turn == 'W':
            self._scoreboard.create_oval(self._scoreboardwidth * 0.5,
                                         self._scoreboardheight * 0.17,
                                         self._scoreboardwidth * 0.5 + self.circlelength,
                                         self._scoreboardheight * 0.17 + self.circlelength,
                                         outline = white_piece,
                                         fill = white_piece)
##        self._redraw_mainboard()
        self._scoreboard.create_oval(self._scoreboardwidth * 0.2,
                                     self._scoreboardheight * 0.36,
                                     self._scoreboardwidth * 0.2 + self.circlelength,
                                     self._scoreboardheight * 0.36 + self.circlelength,
                                     outline = black_piece,
                                     fill = black_piece)
        self._scoreboard.create_text(self._scoreboardwidth * 0.6,
                             self._scoreboardheight * 0.4,
                             font = DEFAULT_FONT,
                             text = ':   ' + str(self._black),
                             fill = font_color)
        self._scoreboard.create_oval(self._scoreboardwidth * 0.2,
                                     self._scoreboardheight * 0.48,
                                     self._scoreboardwidth * 0.2 + self.circlelength,
                                     self._scoreboardheight * 0.48 + self.circlelength,
                                     outline = white_piece,
                                     fill = white_piece)
        self._scoreboard.create_text(self._scoreboardwidth * 0.6,
                             self._scoreboardheight * 0.52,
                             font = DEFAULT_FONT,
                             text = ':   ' + str(self._white),
                             fill = font_color)
        self._scoreboard.create_rectangle(self._scoreboardwidth * 0.15,
                                  self._scoreboardheight * 0.7,
                                  self._scoreboardwidth * 0.85,
                                  self._scoreboardheight * 0.9,
                                  outline = line_color)


    def _drop_piece(self, event: tkinter.Event):
        position = self._position(event.x, event.y)
        if position != None:
            try:
                self._redraw_mainboard()
                self._redraw_scoreboard()
                self._state.victory_condition()
                self._state.double_illegal()
                self._state.check_move()
            except F.GameOverError:
                self._newroot = tkinter.Tk()
                self._newroot.title('Game Over!')
                if self._victory_condition == 'The most discs wins':
                    gameover = tkinter.Label(master = self._newroot,
                                             text = 'Game Over. {}'.format(self._state.winner()))
                elif self._victory_condition == 'The fewest discs wins':
                    gameover = tkinter.Label(master = self._newroot,
                                             text = 'Game Over. {}'.format(self._state.inverse_winner()))                                            
                gameover.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
                restart = tkinter.Label(master = self._newroot,
                                         text = 'Play again?')
                restart.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)
                Y = tkinter.Button(master = self._newroot, text = ' Yes ', command = self._restart)
                Y.grid(row = 2, column = 0, padx = 20, pady = 20)
                N = tkinter.Button(master = self._newroot, text = ' No ', command = self._end_game)
                N.grid(row = 2, column = 1, padx = 20, pady = 20)
            except F.NoLegalMoveError:
                self._turn = F.change_turn(self._turn)
                self._redraw_scoreboard()
                self._information()


    def _information(self):
        '''draw an information on the board'''
        self._message_box1 = '{} player has\nno legal place\nto drop piece.'.format(F.full_name(F.change_turn(self._turn)))
        self._scoreboard.create_text(self._scoreboardwidth * 0.5,
                             self._scoreboardheight * 0.8,
                             font = ('Helvetica', 10),
                             text = self._message_box1,
                             fill = font_color)


    def _position(self, eventx: int, eventy: int):
        '''takes the position of the mouse, returns the location of the
        board; returns None if mouse if not on the window'''
        for i in range(self._rows):
            for n in range(self._columns):
                if self._coordinates[i][n][0] < eventx < self._coordinates[i][n][2]\
                   and self._coordinates[i][n][1] < eventy < self._coordinates[i][n][3]:
                    return (i,n)
        return None

    def _on_mouse_pressed(self, event: tkinter.Event):
        x = event.x
        y = event.y
        position = self._position(x, y)
        if position != None:
            try:
##                self._scoreboard.delete(self._invalid)
##                self._scoreboard.delete(self._change)
                self._state.make_move(position[0] + 1, position[1] + 1)
                self._turn = F.change_turn(self._turn)
            except F.InvalidMoveError:
                if self._highlighter_exist == True:
                    self._redraw_mainboard()
                    self._redraw_scoreboard()
                self._draw_invalid_highlighter(position[0],position[1])
            else:
                pass

    def _restart(self):
        '''used in the error window'''
        self._newroot.destroy()
        self._game_window.destroy()
        game = OthelloGame(launcher)
        game.start()

    def _end_game(self):
        self._newroot.destroy()
        self._game_window.destroy()

    def _on_mouse_moved(self, event: tkinter.Event):
        x = event.x
        y = event.y
        position = self._position(x,y)
        if position != None:
            if self._board[position[0]][position[1]] == '*':
                self._draw_highlighter(position[0], position[1])
        else:
            if self._highlighter_exist == True:
                self._redraw_mainboard()
                self._redraw_scoreboard()
                self._highlighter_exist = False

    def _draw_highlighter(self, r: int, c:int):
        '''create a frame that indicate which blank are you pointing'''
        if self._highlighter_exist == True:
            self._redraw_mainboard()
        self._canvas.create_rectangle(self._coordinates[r][c][0],
                                     self._coordinates[r][c][1],
                                     self._coordinates[r][c][2],
                                     self._coordinates[r][c][3],
                                     outline = 'white')
        self._highlighter_exist = True


    def _draw_invalid_highlighter(self, r: int, c: int):
        '''create an X mark when this move is invalid'''
        if self._highlighter_exist == True:
            self._redraw_mainboard()
        self._massage_box = 'Invalid Move.'
        self._scoreboard.create_text(self._scoreboardwidth * 0.5,
                     self._scoreboardheight * 0.8,
                     font = ('Helvetica', 12),
                     text = self._massage_box,
                     fill = font_color)
        self._canvas.create_rectangle(self._coordinates[r][c][0],
                                     self._coordinates[r][c][1],
                                     self._coordinates[r][c][2],
                                     self._coordinates[r][c][3],
                                     outline = 'red')
        self._canvas.create_line(self._coordinates[r][c][0],
                                self._coordinates[r][c][1],
                                self._coordinates[r][c][2],
                                self._coordinates[r][c][3],
                                fill = 'red')
        self._canvas.create_line(self._coordinates[r][c][0],
                                self._coordinates[r][c][3],
                                self._coordinates[r][c][2],
                                self._coordinates[r][c][1],
                                fill = 'red')
        self._highlighter_exist = True


    def start(self) -> None:
        self._game_window.mainloop()



##please make sure not to run this module under python 3.3.5



if __name__ == '__main__':
    launcher = launcher.Launcher()
    game = OthelloGame(launcher)
    game.start()






