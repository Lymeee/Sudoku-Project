import pygame, copy
import sys
from sudoku_generator import *



class Board:
    def __init__(self, width, height, screen, difficulty):
        pass
    def generate_board(self):
        pass
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
        pass
    def set_cell_value(self, value):
        pass
    def draw(self):
        pass
def draw_button(screen, button, button_name):
    pass