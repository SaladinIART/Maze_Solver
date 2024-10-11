import pygame
import sys
from collections import deque
import heapq

# Colors
WHITE = (255, 255, 255)  # Path
GREY = (128, 128, 128)  # Wall
START_COLOR = (0, 0, 255)  # Start (Blue)
GOAL_COLOR = (255, 0, 0)  # Goal (Red)
ROBOT_COLOR = (0, 255, 0)  # Robot (Green)
VISITED_COLOR = (100, 100, 255)  # Visited nodes (Light blue)
PATH_COLOR = (255, 255, 0)  # Final path (Yellow)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((560, 1000))  # Set the window size to accommodate the larger maze
pygame.display.set_caption("Pygame Maze Solver - Extended Complex Maze")

# Start and Goal positions
start_pos = (20, 20)  # Top-left corner
goal_pos = (500, 960)  # Near the bottom-right corner

# Extended Complex Maze Layout Representation (0 = Path, 1 = Wall)
complex_maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # Adding additional rows with similar complexity
]

for _ in range(35):  # Add 35 more rows to make the total number of rows 50
    complex_maze.append([1, 0] + [0, 1] * 13 + [1])

# Function to draw the extended complex maze
def draw_complex_maze():
    cell_size = 20  # Each cell is 20x20 pixels
    for row_index, row in enumerate(complex_maze):
        for col_index, value in enumerate(row):
            color = WHITE  # Default to path
            if value == 1:
                color = GREY  # Wall
            
            pygame.draw.rect(screen, color, (col_index * cell_size, row_index * cell_size, cell_size, cell_size))

    # Draw Start and Goal
    pygame.draw.rect(screen, START_COLOR, (start_pos[0], start_pos[1], cell_size, cell_size))
    pygame.draw.rect(screen, GOAL_COLOR, (goal_pos[0], goal_pos[1], cell_size, cell_size))

# Main game loop for visualizing the extended complex maze
while True:
    screen.fill(GREY)  # Background is grey to represent the walls more clearly
    draw_complex_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
