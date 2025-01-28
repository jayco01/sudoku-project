import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 540, 540
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
FONT = pygame.font.Font(None, 36)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # Extra space for the menu
pygame.display.set_caption("Sudoku")

# Function to check if a number is valid in the 3x3 grid
def is_valid_subgrid(grid, row, col, num):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i != row or j != col) and grid[i][j] == num:
                return False
    return True

# Function to check if a number is valid globally
def is_valid_global(grid, row, col, num):
    for i in range(GRID_SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    return is_valid_subgrid(grid, row, col, num)

# Function to generate a valid Sudoku grid using backtracking
def generate_valid_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    nums = list(range(1, 10))

    def backtrack():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid_global(grid, row, col, num):
                            grid[row][col] = num
                            if backtrack():
                                return True
                            grid[row][col] = 0
                    return False
        return True

    backtrack()
    return grid

# Function to validate the grid after removing numbers
def is_grid_valid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            if num != 0:
                grid[row][col] = 0
                if not is_valid_global(grid, row, col, num):
                    grid[row][col] = num
                    return False
                grid[row][col] = num
    return True

# Function to remove numbers to create a puzzle
def create_puzzle(grid, blanks=40, max_attempts=100):
    for attempt in range(max_attempts):
        puzzle = [row[:] for row in grid]
        positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
        random.shuffle(positions)

        removed = 0
        for r, c in positions:
            if removed >= blanks:
                break
            temp = puzzle[r][c]
            puzzle[r][c] = 0
            if not is_grid_valid(puzzle):
                puzzle[r][c] = temp
            else:
                removed += 1

        if removed == blanks:
            return puzzle

    return create_puzzle(generate_valid_grid(), blanks, max_attempts)

# Function to generate modifiable grid
def generate_modifiable_grid(puzzle):
    return [[cell == 0 for cell in row] for row in puzzle]

# Generate a new puzzle on game start
solution = generate_valid_grid()
puzzle = create_puzzle(solution, blanks=40)
grid = [row[:] for row in puzzle]
modifiable_grid = generate_modifiable_grid(grid)

# Selected cell
selected_cell = None

# Error mode toggle
error_mode = True

def draw_grid():
    for x in range(0, WIDTH + 1, CELL_SIZE):
        is_subgrid_line = (x // CELL_SIZE) % 3 == 0
        pygame.draw.line(screen, BLACK if is_subgrid_line else GRAY, (x, 0), (x, HEIGHT), 3 if is_subgrid_line else 1)
    for y in range(0, HEIGHT + 1, CELL_SIZE):
        is_subgrid_line = (y // CELL_SIZE) % 3 == 0
        pygame.draw.line(screen, BLACK if is_subgrid_line else GRAY, (0, y), (WIDTH, y), 3 if is_subgrid_line else 1)

def draw_numbers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            if num != 0:
                color = BLACK
                if error_mode and modifiable_grid[row][col] and not is_valid_subgrid(grid, row, col, num):
                    color = RED
                elif not modifiable_grid[row][col]:
                    color = BLUE
                text = FONT.render(str(num), True, color)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 4))

def highlight_cell():
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(
            screen, GREEN,
            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            3
        )

def draw_menu():
    menu_text = f"Error Mode: {'ON' if error_mode else 'OFF'}"
    text = FONT.render(menu_text, True, BLACK)
    screen.blit(text, (10, HEIGHT + 10))

def toggle_error_mode():
    global error_mode
    error_mode = not error_mode

def select_cell(pos):
    global selected_cell
    x, y = pos
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        selected_cell = y // CELL_SIZE, x // CELL_SIZE
    else:
        selected_cell = None

def insert_number(number):
    if selected_cell:
        row, col = selected_cell
        if modifiable_grid[row][col]:
            grid[row][col] = number

def erase_number():
    if selected_cell:
        row, col = selected_cell
        if modifiable_grid[row][col]:
            grid[row][col] = 0

def is_puzzle_solved():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != solution[row][col]:
                return False
    return True

def display_message(message):
    text = FONT.render(message, True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_numbers()
    highlight_cell()
    draw_menu()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[1] > HEIGHT:
                toggle_error_mode()
            else:
                select_cell(pos)
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isdigit() and event.unicode != '0':
                insert_number(int(event.unicode))
                if is_puzzle_solved():
                    display_message("Congratulations! You solved it!")
                    running = False
            elif event.key == pygame.K_BACKSPACE:
                erase_number()

pygame.quit()
sys.exit()
