import pygame
import sys

# Constants
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 2
BOLD_LINE_WIDTH = 4
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)

class Cell:
    def __init__(self, value, row, col, screen):
        pass

    def set_cell_value(self, value):
        pass

    def set_sketched_value(self, value):
        pass

    def draw(self):
        pass

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.board = [[Cell(0, i, j, screen) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        self.selected_cell = None

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        # makes the cells
        for row in self.board:
            for cell in row:
                cell.draw()

        # makes the grid lines
        for i in range(GRID_SIZE + 1):
            line_width = BOLD_LINE_WIDTH if i % 3 == 0 else LINE_WIDTH
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.board[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if x < self.width and y < self.height:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            self.select(row, col)

    def clear(self):
        if self.selected_cell:
            self.selected_cell.set_cell_value(0)

    def sketch(self, value):
        # placeholder
        pass

    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        for row in self.board:
            for cell in row:
                cell.set_cell_value(0)

    def is_full(self):
        return all(cell.value != 0 for row in self.board for cell in row)

    def update_board(self):
        pass

    def find_empty(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j].value == 0:
                    return (i, j)
        return None

    def check_board(self):
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    board = Board(WIDTH, HEIGHT, screen, "easy")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                board.click(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    board.place_number(1)
                elif event.key == pygame.K_2:
                    board.place_number(2)
                elif event.key == pygame.K_3:
                    board.place_number(3)
                elif event.key == pygame.K_4:
                    board.place_number(4)
                elif event.key == pygame.K_5:
                    board.place_number(5)
                elif event.key == pygame.K_6:
                    board.place_number(6)
                elif event.key == pygame.K_7:
                    board.place_number(7)
                elif event.key == pygame.K_8:
                    board.place_number(8)
                elif event.key == pygame.K_9:
                    board.place_number(9)
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()

        board.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
