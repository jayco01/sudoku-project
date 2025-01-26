import pygame
import sys

# Initialize Pygame
pygame.init()

# screen dimensions
WIDTH, HEIGHT = 540, 540
GRID_SIZE = 9
CELL_SIZE = WIDTH //GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (173, 216, 230)

# Font
FONT = pygame.font.Font(None, 36)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# A 2D list to store the grid (0 represents an empty cell)
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Create a modifiable grid (True for editable cells, False for fixed cells)
modifiable_grid = [[cell == 0 for cell in row] for row in grid]

# selected cell
selected_cell = None

# Function to draw the grid
def draw_grid():
    """Draw the Sudoku grid."""
    # Draw vertical lines (x-coordinates determine position)
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK if x % 3 == 0 else GRAY, (x, 0), (x, HEIGHT), 2 if x % 3 == 0 else 1)
    
    # Draw horizontal lines (y-coordinates determine position)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK if y % 3 == 0 else GRAY, (0, y), (WIDTH, y), 2 if y % 3 == 0 else 1)

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

pygame.quit()
sys.exit()
