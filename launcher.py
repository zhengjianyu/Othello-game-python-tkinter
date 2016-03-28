#  Jianyu Zheng 33062456.  ICS 32 Lab sec 5.  Lab asst 5.


import tkinter
from tkinter import ttk



class InvalidSizeError(Exception):
    '''raised when the chessboard is oversized or too small'''
    pass


class InputError(Exception):
    '''raised when the user input is invalid'''
    pass


class Launcher:
    '''collection of functions about Reversi launcher'''
    def __init__(self):
        self._DEFAULT_FONT = ('Helvetica', 20)
        self._root = tkinter.Tk()
        self._root.title('Game Launcher')
        WelcomeLabel = tkinter.Label(master = self._root, text = 'Welcome to Othello!')
        WelcomeLabel.grid(row = 0, column = 0, columnspan = 2, padx = 0, pady = 10, sticky = 'wesn')
        OptionsLabel = tkinter.Label(master = self._root, text = 'Please select the options below :)')
        OptionsLabel.grid(row = 1, column = 0, columnspan = 2, padx = 0, pady = 10, sticky = 'wesn')
        self._L1 = tkinter.Label(text = 'Enter the number of rows:')
        self._L1.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'wesn')
        self._E1 = tkinter.Entry(bd = 4)
        self._E1.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'wesn')
        self._L2 = tkinter.Label(text = 'Enter the number of columns:')
        self._L2.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'wesn')
        self._E2 = tkinter.Entry(bd = 4)
        self._E2.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'wesn')
        self._L3 = tkinter.Label(text = 'Select a player who will move first:')
        self._L3.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'wesn')
        self._V3 = tkinter.StringVar()
        self._V3.set('Black Player')
        self._E3 = ttk.Combobox(textvariable = self._V3, values = ['Black Player', 'White Player'])
        self._E3.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'wesn')
        self._L4 = tkinter.Label(text = "Select the top-left center cell's color:")
        self._L4.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'wesn')
        self._V4 = tkinter.StringVar()
        self._V4.set('Black')
        self._E4 = ttk.Combobox(textvariable = self._V4, values = ['Black', 'White'])
        self._E4.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = 'wesn')
        self._L5 = tkinter.Label(text = 'Select a victory condition:')
        self._L5.grid(row = 6, column = 0, padx = 10, pady = 10, sticky = 'wesn')
        self._V5 = tkinter.StringVar()
        self._V5.set('The most discs wins')
        self._E5 = ttk.Combobox(textvariable = self._V5, values = ['The most discs wins', 'The fewest discs wins'])
        self._E5.grid(row = 6, column = 1, padx = 10, pady = 10, sticky = 'wesn')
        self._button = tkinter.Button(master = self._root, text = ' OK ',
                                      command = self._on_button_pressed,
                                      font = self._DEFAULT_FONT)
        self._button.grid(row = 7, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'n')
        self._root.rowconfigure(0, weight = 1)
        self._root.rowconfigure(1, weight = 1)
        self._root.rowconfigure(2, weight = 1)
        self._root.rowconfigure(3, weight = 1)
        self._root.rowconfigure(4, weight = 1)
        self._root.rowconfigure(5, weight = 1)
        self._root.rowconfigure(6, weight = 1)
        self._root.columnconfigure(0, weight = 1)
        self._root.columnconfigure(1, weight = 1)

        
    def _on_button_pressed(self) -> None:
        row = self._E1.get()
        column = self._E2.get()
        option1 = self._E3.get()
        option2 = self._E4.get()
        option3 = self._E5.get()
        try:
            if not 4 <= int(column) <= 16 or not 4 <= int(row) <= 16:
                raise InvalidSizeError()
            elif int(column) % 2 != 0 or int(row) % 2 != 0:
                raise InputError()
            self._result = [int(row), int(column), option1, option2, option3]
            self._root.destroy()
            return self._result
        except ValueError:
            self._newroot = tkinter.Tk()
            self._newroot.title('Error!')
            warning1 = tkinter.Label(master = self._newroot, text = 'Wrong input. Please try again.')
            warning1.grid(row = 0, column = 0, padx = 10, pady = 10)
            accept = tkinter.Button(master = self._newroot, text = ' OK ', command = self._close_it)
            accept.grid(row = 2, column = 0, padx = 20, pady = 20)
        except InvalidSizeError:
            self._newroot = tkinter.Tk()
            self._newroot.title('Error!')
            warning1 = tkinter.Label(master = self._newroot, text = 'Wrong size. The side length of chessboard should between 4 to 16.')
            warning1.grid(row = 0, column = 0, padx = 10, pady = 10)
            warning2 = tkinter.Label(master = self._newroot, text = 'Please try again.')
            warning2.grid(row = 1, column = 0, padx = 10, pady = 10)
            accept = tkinter.Button(master = self._newroot, text = ' OK ', command = self._close_it)
            accept.grid(row = 2, column = 0, padx = 20, pady = 20)
        except InputError:
            self._newroot = tkinter.Tk()
            self._newroot.title('Error!')
            warning1 = tkinter.Label(master = self._newroot, text = 'Wrong number. The side length of chessboard should be even numbers.')
            warning1.grid(row = 0, column = 0, padx = 10, pady = 10)
            warning2 = tkinter.Label(master = self._newroot, text = 'Please try again.')
            warning2.grid(row = 1, column = 0, padx = 10, pady = 10)
            accept = tkinter.Button(master = self._newroot, text = ' OK ', command = self._close_it)
            accept.grid(row = 2, column = 0, padx = 20, pady = 20)
            
    def _close_it(self):
        '''used in the error window'''
        self._newroot.destroy()

    def start(self):
        self._root.mainloop()
        return self._result
        



##a = Launcher()
##a.start()
