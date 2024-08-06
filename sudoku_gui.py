import pygame
import sys
from sudoku_generator import generate_sudoku

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 1000
BOARD_SIZE = 900
GRID_SIZE = 9
CELL_SIZE = BOARD_SIZE // GRID_SIZE
LINE_WIDTH = 2
BOLD_LINE_WIDTH = 4
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)
HIGHLIGHT_COLOR = (186, 85, 211)
HIGHLIGHT_WIDTH = 5
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60

difficulty_levels = {
    'easy': 1,
    'medium': 40,
    'hard': 60
}
# Initialize the pygame and create font.
pygame.font.init()
FONT = pygame.font.SysFont('arial', 36)
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.is_initial = value != 0

    def set_cell_value(self, value):
        if not self.is_initial: # so changes can't be made to other cells
            self.value = value

    def set_sketched_value(self, value):
        if not self.is_initial: # same as above
            self.sketched_value = value

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, rect)
        if self.value != 0:
            text_color = LINE_COLOR if self.is_initial else (0, 0, 255)  # Different color for user input
            text = FONT.render(str(self.value), True, text_color)
            self.screen.blit(text, (x + CELL_SIZE // 2 - text.get_width() // 2, y + CELL_SIZE // 2 - text.get_height() // 2))
        elif self.sketched_value != 0:
            text = FONT.render(str(self.sketched_value), True, LINE_COLOR)
            self.screen.blit(text, (x + 5, y + 5))
        if self.selected:
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, rect, HIGHLIGHT_WIDTH)

class Board:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.difficulty = difficulty_levels[difficulty]
        self.board = [[Cell(0, i, j, screen) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        self.selected_cell = None
        self.selected_row = 0
        self.selected_col = 0
        self.solution = None

    def initialize_board(self):
        puzzle, self.solution = generate_sudoku(GRID_SIZE, self.difficulty)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = self.board[i][j]
                cell.set_cell_value(puzzle[i][j])
                cell.is_initial = puzzle[i][j] != 0  # Mark initial puzzle cells

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in self.board:
            for cell in row:
                cell.draw()
        for i in range(GRID_SIZE + 1):
            line_width = BOLD_LINE_WIDTH if i % 3 == 0 else LINE_WIDTH
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), line_width)
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), line_width)

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.board[row][col]
        self.selected_cell.selected = True
        self.selected_row, self.selected_col = row, col

    def arrow_selection(self, dx, dy):
        new_row = (self.selected_row + dy) % GRID_SIZE
        new_col = (self.selected_col + dx) % GRID_SIZE
        self.select(new_row, new_col)

    def click(self, x, y):
        if x < BOARD_SIZE and y < BOARD_SIZE:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            self.select(row, col)

    def clear(self):
        if self.selected_cell:
            self.selected_cell.set_cell_value(0)

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        for row in self.board:
            for cell in row:
                if not cell.is_initial:  # Only reset cells that are not part of the initial puzzle
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
        # Check if current board matches the solution
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j].value != self.solution[i][j]:
                    return False
        return True

def start_game(screen, difficulty):
    board = Board(screen, difficulty)
    board.initialize_board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
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
                elif event.key == pygame.K_UP:
                    board.arrow_selection(0, -1)
                elif event.key == pygame.K_DOWN:
                    board.arrow_selection(0, 1)
                elif event.key == pygame.K_LEFT:
                    board.arrow_selection(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    board.arrow_selection(1, 0)

        board.draw()
        button_rects = draw_buttons(screen)
        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # Left mouse button
            if button_rects[0].collidepoint(mouse_pos):
                board.reset_to_original()
            elif button_rects[1].collidepoint(mouse_pos):
                main()
            elif button_rects[2].collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

        # Check for win or loss condition
        if board.is_full():
            if board.check_board():
                end_game(screen, "won")
            else:
                end_game(screen, "lost")

def end_game(screen, result):
    screen.fill((255, 255, 255))
    pygame.display.flip()

    # Initialize ending screen fonts
    ending_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 60)

    if result == "won":
        # Player wins the sudoku game
        winner_surface = ending_font.render('Game Won!', True, (0, 0, 0))
        screen.blit(winner_surface, (275, 350))
    else:
        # Player loses the sudoku game
        loser_surface = ending_font.render('Game Over :(', True, (0, 0, 0))
        screen.blit(loser_surface, (260, 350))

    # Exit button
    exit_button_surface = pygame.Surface((250, 150))
    pygame.draw.rect(exit_button_surface, (0, 0, 0), exit_button_surface.get_rect(), 3)
    exit_text = button_font.render('EXIT', True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(exit_button_surface.get_width() / 2, exit_button_surface.get_height() / 2))
    exit_button_surface.blit(exit_text, exit_rect)
    exit_button_rect = pygame.Rect(350, 550, 250, 150)
    screen.blit(exit_button_surface, (350, 550))

    # Restart button
    res_button_surface = pygame.Surface((250, 150))
    pygame.draw.rect(res_button_surface, (0, 0, 0), res_button_surface.get_rect(), 3)
    res_text = button_font.render('RESTART', True, (255, 255, 255))
    res_rect = res_text.get_rect(center=(res_button_surface.get_width() / 2, res_button_surface.get_height() / 2))
    res_button_surface.blit(res_text, res_rect)
    res_button_rect = pygame.Rect(350, 750, 250, 150)
    screen.blit(res_button_surface, (350, 750))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif res_button_rect.collidepoint(event.pos):
                    main()

def draw_buttons(screen):
    button_font = pygame.font.Font(None, 45)

    buttons = ['RESET', 'RESTART', 'EXIT']
    button_rects = []

    total_button_width = BUTTON_WIDTH * len(buttons)
    total_spacing = WINDOW_WIDTH - total_button_width
    spacing = total_spacing // (len(buttons) + 1)

    for i, button_text in enumerate(buttons):
        button_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(button_surface, (0, 0, 0), button_surface.get_rect(), 3)
        text = button_font.render(button_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(button_surface.get_width() / 2, button_surface.get_height() / 2))
        button_surface.blit(text, text_rect)

        button_x = spacing * (i + 1) + BUTTON_WIDTH * i
        button_rect = pygame.Rect(button_x, BOARD_SIZE + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rects.append(button_rect)

        screen.blit(button_surface, button_rect.topleft)

    return button_rects

def main():
    # initializing pygame module, making game window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Sudoku')

    # Sudoku title: initialized, rendered, updated to screen
    title_font = pygame.font.Font(None, 100)
    title_surface = title_font.render('Sudoku', True, (0, 0, 0))
    screen.blit(title_surface, (350, 300))

    # Select difficulty message: initialized, rendered, updated to screen
    difficulty_selection = pygame.font.Font(None, 65)
    difficulty_surface = difficulty_selection.render('Select Game Mode:', True, (0, 0, 0))
    screen.blit(difficulty_surface, (265, 450))
    pygame.display.flip()

    button_font = pygame.font.Font(None, 45)

    # Easy Button
    easy_button_surface = pygame.Surface((150, 200))
    pygame.draw.rect(easy_button_surface, (0, 0, 0), easy_button_surface.get_rect(), 3)
    easy_text = button_font.render('EASY', True, (255, 255, 255))
    easy_rect = easy_text.get_rect(center=(easy_button_surface.get_width() / 2, easy_button_surface.get_height() / 2))
    easy_button_surface.blit(easy_text, easy_rect)
    easy_button_rect = pygame.Rect(75, 600, 150, 200)
    screen.blit(easy_button_surface, (75, 600))

    # Medium Button
    med_button_surface = pygame.Surface((150, 200))
    pygame.draw.rect(med_button_surface, (0, 0, 0), med_button_surface.get_rect(), 3)
    med_text = button_font.render('MEDIUM', True, (255, 255, 255))
    med_rect = med_text.get_rect(center=(med_button_surface.get_width() / 2, med_button_surface.get_height() / 2))
    med_button_surface.blit(med_text, med_rect)
    med_button_rect = pygame.Rect(375, 600, 150, 200)
    screen.blit(med_button_surface, (375, 600))

    # Hard Button
    hard_button_surface = pygame.Surface((150, 200))
    pygame.draw.rect(hard_button_surface, (0, 0, 0), hard_button_surface.get_rect(), 3)
    hard_text = button_font.render('HARD', True, (255, 255, 255))
    hard_rect = hard_text.get_rect(center=(hard_button_surface.get_width() / 2, hard_button_surface.get_height() / 2))
    hard_button_surface.blit(hard_text, hard_rect)
    hard_button_rect = pygame.Rect(675, 600, 150, 200)
    screen.blit(hard_button_surface, (675, 600))
    pygame.display.flip()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            # checks for specific quit event
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_button_rect.collidepoint(event.pos):
                    screen.fill((255, 255, 255))
                    pygame.display.flip()
                    start_game(screen, 'easy')
                elif med_button_rect.collidepoint(event.pos):
                    screen.fill((255, 255, 255))
                    pygame.display.flip()
                    start_game(screen, 'medium')
                elif hard_button_rect.collidepoint(event.pos):
                    screen.fill((255, 255, 255))
                    pygame.display.flip()
                    start_game(screen, 'hard')

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()