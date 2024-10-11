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
screen = pygame.display.set_mode((560, 560))  # Increase size to accommodate larger maze
pygame.display.set_caption("Pygame Maze Solver - Complex Maze")

# Start and Goal positions (Updated)
start_pos = (20, 380)  # A20 (Row 20, Column 1)
goal_pos = (520, 140)  # AB10 (Row 10, Column 28)

# Complex Maze Layout Representation (0 = Path, 1 = Wall)
complex_maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]

# Function to draw the complex maze
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

# BFS Implementation
def bfs(start, goal):
    queue = deque([start])
    visited = set()
    parents = {}

    visited.add(start)
    while queue:
        current = queue.popleft()

        # Visualize the current node
        pygame.draw.rect(screen, VISITED_COLOR, (current[0], current[1], 20, 20))
        pygame.display.flip()
        pygame.time.delay(50)

        if current == goal:
            reconstruct_path(parents, start, goal)
            return

        neighbors = [
            (current[0] + dx, current[1] + dy) for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]
        ]

        for neighbor in neighbors:
            # Ensure neighbor is within bounds of the grid and is not an obstacle
            if 0 <= neighbor[0] // 20 < len(complex_maze[0]) and 0 <= neighbor[1] // 20 < len(complex_maze):
                if neighbor not in visited and neighbor not in obstacles:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parents[neighbor] = current

# DFS Implementation
def dfs(start, goal):
    stack = [start]
    visited = set()
    parents = {}

    visited.add(start)
    while stack:
        current = stack.pop()

        # Visualize the current node
        pygame.draw.rect(screen, VISITED_COLOR, (current[0], current[1], 20, 20))
        pygame.display.flip()
        pygame.time.delay(50)

        if current == goal:
            reconstruct_path(parents, start, goal)
            return

        neighbors = [
            (current[0] + dx, current[1] + dy) for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]
        ]

        for neighbor in neighbors:
            # Ensure neighbor is within bounds of the grid and is not an obstacle
            if 0 <= neighbor[0] // 20 < len(complex_maze[0]) and 0 <= neighbor[1] // 20 < len(complex_maze):
                if neighbor not in visited and neighbor not in obstacles:
                    stack.append(neighbor)
                    visited.add(neighbor)
                    parents[neighbor] = current

# A* Implementation
def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    g_cost = {start: 0}
    parents = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        # Visualize the current node
        pygame.draw.rect(screen, VISITED_COLOR, (current[0], current[1], 20, 20))
        pygame.display.flip()
        pygame.time.delay(50)

        if current == goal:
            reconstruct_path(parents, start, goal)
            return

        neighbors = [
            (current[0] + dx, current[1] + dy) for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]
        ]

        for neighbor in neighbors:
            # Ensure neighbor is within bounds of the grid and is not an obstacle
            if 0 <= neighbor[0] // 20 < len(complex_maze[0]) and 0 <= neighbor[1] // 20 < len(complex_maze):
                if neighbor not in obstacles:
                    tentative_g_cost = g_cost[current] + 1

                    if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                        g_cost[neighbor] = tentative_g_cost
                        f_cost = tentative_g_cost + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_cost, neighbor))
                        parents[neighbor] = current
                        
# Function to reconstruct path
def reconstruct_path(parents, start, goal):
    current = goal
    while current != start:
        current = parents[current]
        pygame.draw.rect(screen, PATH_COLOR, (current[0], current[1], 20, 20))
        pygame.display.flip()
        pygame.time.delay(50)

# Main game loop for visualizing the complex maze
while True:
    screen.fill(GREY)  # Background is grey to represent the walls more clearly
    draw_complex_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Press 'b' to start BFS
                bfs(start_pos, goal_pos)

    pygame.display.flip()