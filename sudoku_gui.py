import pygame, copy
import sys
from sudoku_generator import *

board_rows = 9
line_color = 52, 110, 235
screen_height = 900 + 100
screen_width = 900
square_size = 100

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.board = None
        self.cells = None
        self.cells_copy = None
        self.selected_cell = (0, 0)
    def generate_board(self):
        self.board, self.cells = generate_sudoku(9, self.difficulty)
        self.cells = [
            [Cell(self.cells[i][j], i, j, square_size, square_size) for j in range(board_rows)]
            for i in range(board_rows)
        ]
    def is_full(self):
        pass
    def draw(self):
        pass
    def select(self, row, col):
        pass
    def click(self, x, y):
        pass
    def arrows(self, direction):
        pass
    def place_number(self, value):
        pass

    def reset_to_original(self):
        pass
    def check_win(self):
        pass
class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    def set_cell_value(self, value):
        pass
    def draw(self):
        pass
def draw_button(screen, button, button_name):
    pass