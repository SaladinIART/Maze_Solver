import pygame
import sys
from collections import deque
import heapq

# Colors
WHITE = (255, 255, 255)  # Path
GREY = (128, 128, 128)  # Wall
START_COLOR = (0, 0, 255)  # Start (Blue)
GOAL_COLOR = (255, 0, 0)  # Goal (Red)
VISITED_COLOR = (100, 100, 255)  # Visited nodes (Light blue)
PATH_COLOR = (255, 255, 0)  # Final path (Yellow)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((560, 560))
pygame.display.set_caption("Pygame Maze Solver - Complex Maze")

# Start and Goal positions
start_pos = (20, 380)
goal_pos = (520, 140)

# Complex Maze Layout
complex_maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]    
    ]

# Convert maze matrix to obstacle set
obstacles = set()
cell_size = 20
for row_index, row in enumerate(complex_maze):
    for col_index, value in enumerate(row):
        if value == 1:
            obstacles.add((col_index * cell_size, row_index * cell_size))

# Function to draw the complex maze
def draw_complex_maze():
    for row_index, row in enumerate(complex_maze):
        for col_index, value in enumerate(row):
            color = WHITE if value == 0 else GREY
            pygame.draw.rect(screen, color, (col_index * cell_size, row_index * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, START_COLOR, (*start_pos, cell_size, cell_size))
    pygame.draw.rect(screen, GOAL_COLOR, (*goal_pos, cell_size, cell_size))

# Function to reconstruct and visualize the path
def reconstruct_path(parents, start, goal):
    current = goal
    while current != start:
        current = parents[current]
        pygame.draw.rect(screen, PATH_COLOR, (current[0], current[1], cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(50)

# Heuristic function for A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# BFS Algorithm
def bfs(start, goal):
    queue = deque([start])
    visited = {start}
    parents = {}

    while queue:
        # Process Pygame events to avoid freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.popleft()
        pygame.draw.rect(screen, VISITED_COLOR, (current[0], current[1], cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(10)

        if current == goal:
            reconstruct_path(parents, start, goal)
            return

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, cell_size), (0, -cell_size), (cell_size, 0), (-cell_size, 0)]]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < 560 and 0 <= neighbor[1] < 560 and neighbor not in visited and neighbor not in obstacles):
                queue.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = current

# DFS Algorithm
def dfs(start, goal):
    stack = [start]
    visited = {start}
    parents = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack.pop()
        pygame.draw.rect(screen, VISITED_COLOR, (current[0], current[1], cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(10)

        if current == goal:
            reconstruct_path(parents, start, goal)
            return

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, cell_size), (0, -cell_size), (cell_size, 0), (-cell_size, 0)]]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < 560 and 0 <= neighbor[1] < 560 and neighbor not in visited and neighbor not in obstacles):
                stack.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = current

# A* Algorithm
def a_star(start, goal):
    open_set = [(0, start)]
    g_cost = {start: 0}
    parents = {}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        _, current = heapq.heappop(open_set)
        pygame.draw.rect(screen, VISITED_COLOR, (current[0], current[1], cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(10)

        if current == goal:
            reconstruct_path(parents, start, goal)
            return

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, cell_size), (0, -cell_size), (cell_size, 0), (-cell_size, 0)]]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < 560 and 0 <= neighbor[1] < 560 and neighbor not in obstacles):
                tentative_g_cost = g_cost[current] + 1
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_cost, neighbor))
                    parents[neighbor] = current

# Main loop
while True:
    screen.fill(GREY)
    draw_complex_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bfs(start_pos, goal_pos)
            elif event.key == pygame.K_d:
                dfs(start_pos, goal_pos)
            elif event.key == pygame.K_a:
                a_star(start_pos, goal_pos)

    pygame.display.flip()