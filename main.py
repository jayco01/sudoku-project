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
RED = (255,0,0)

# Font
FONT = pygame.font.Font(None, 36)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Function to check if a number is valid in the grid
def is_valid(grid, row, col, num):
    """Check if a number is valid in the current position."""
    for i in range(GRID_SIZE):
        if grid[row][i] == num or grid[i][col] == num:  # Check row and column
            return False
    
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True

# Function to generate a valid Sudoku grid using backtracking
def generate_valid_grid():
    """Generate a complete valid Sudoku grid."""
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Start with an empty grid
    nums = list(range(1, 10))
    random.shuffle(nums)  # Shuffle numbers for randomness

    def backtrack():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:  # Find an empty cell
                    random.shuffle(nums)  # Shuffle numbers to randomize solutions
                    for num in nums:
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if backtrack():
                                return True
                            grid[row][col] = 0  # Reset cell if no solution found
                    return False
        return True

    backtrack()
    return grid

# Function to remove numbers to create a puzzle
def create_puzzle(grid, blanks=40):
    """Remove numbers from the grid to create a puzzle."""
    puzzle = [row[:] for row in grid]  # Make a copy of the grid
    positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(positions)

    for i in range(blanks):
        r, c = positions[i]
        puzzle[r][c] = 0  # Set cell to empty
    return puzzle

# Function to generate modifiable grid
def generate_modifiable_grid(puzzle):
    """Create a modifiable grid to track editable cells."""
    return [[cell == 0 for cell in row] for row in puzzle]

# Generate a new puzzle on game start
solution = generate_valid_grid()  # Generate a complete Sudoku grid
grid = create_puzzle(solution, blanks=40)  # Create a puzzle with blank cells
modifiable_grid = generate_modifiable_grid(grid)

# Selected cell
selected_cell = None

def draw_grid():
    """Draw the Sudoku grid."""
    for x in range(0, WIDTH + 1, CELL_SIZE):
        is_subgrid_line = (x // CELL_SIZE) % 3 == 0
        pygame.draw.line(screen, BLACK if is_subgrid_line else GRAY, (x, 0), (x, HEIGHT), 3 if is_subgrid_line else 1)
    for y in range(0, HEIGHT + 1, CELL_SIZE):
        is_subgrid_line = (y // CELL_SIZE) % 3 == 0
        pygame.draw.line(screen, BLACK if is_subgrid_line else GRAY, (0, y), (WIDTH, y), 3 if is_subgrid_line else 1)

def draw_numbers():
    """Draw the numbers on the grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            if num != 0:
                # Use a different color for fixed vs editable cells
                color = BLACK if not modifiable_grid[row][col] else BLUE
                text = FONT.render(str(num), True, color)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 4))

def highlight_cell():
    """Highlight the selected cell."""
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(
            screen, BLUE, 
            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 
            3
        )

def select_cell(pos):
    """Select a cell based on mouse position."""
    global selected_cell
    x, y = pos
    selected_cell = y // CELL_SIZE, x // CELL_SIZE

def insert_number(number):
    """Insert a number into the selected cell."""
    if selected_cell:
        row, col = selected_cell
        # Allow changes only to modifiable cells
        if modifiable_grid[row][col]:
            grid[row][col] = number

def erase_number():
    """Erase the number in the selected cell."""
    if selected_cell:
        row, col = selected_cell
        if modifiable_grid[row][col]:
            grid[row][col] = 0  # Set the cell to empty

# *** New function: Check if the puzzle is solved ***
def is_puzzle_solved():
    """Check if the current grid matches the solution."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != solution[row][col]:  # Compare with the solution
                return False  # If any cell doesn't match, the puzzle isn't solved
    return True  # All cells match, puzzle is solved

# *** New function: Display a congratulatory message ***
def display_message(message):
    """Display a message on the screen."""
    text = FONT.render(message, True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Pause for 3 seconds before exiting

# Game loop
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_numbers()
    highlight_cell()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            select_cell(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isdigit() and event.unicode != '0':  # Only accept digits 1-9
                insert_number(int(event.unicode))
                if is_puzzle_solved():  # Check if the puzzle is solved
                    display_message("Congratulations! You solved it!")
                    running = False  # End the game loop
            elif event.key == pygame.K_BACKSPACE:  # Handle Backspace key
                erase_number()

pygame.quit()
sys.exit()
