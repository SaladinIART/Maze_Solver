import pygame
import sys
from collections import deque
import heapq

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
START_COLOR = (0, 0, 255)
GOAL_COLOR = (255, 0, 0)
ROBOT_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (169, 169, 169)
VISITED_COLOR = (100, 100, 255)
PATH_COLOR = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((560, 400))
pygame.display.set_caption("Pygame Maze Solver")

# Start, Goal, and Obstacles
start_pos = (0, 0)
goal_pos = (540, 380)
obstacles = [(100, 100), (120, 140), (180, 200)]  # Example obstacle positions

# Function to draw grid
def draw_grid():
    for x in range(0, 560, 20):  # 28 columns
        for y in range(0, 400, 20):  # 20 rows
            rect = pygame.Rect(x, y, 20, 20)
            pygame.draw.rect(screen, WHITE, rect, 1)  # 1 means border thickness

# Function to draw start, goal, and obstacles
def draw_elements():
    # Draw Start
    pygame.draw.rect(screen, START_COLOR, (start_pos[0], start_pos[1], 20, 20))
    # Draw Goal
    pygame.draw.rect(screen, GOAL_COLOR, (goal_pos[0], goal_pos[1], 20, 20))
    # Draw Obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obs[0], obs[1], 20, 20))

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
            if 0 <= neighbor[0] < 560 and 0 <= neighbor[1] < 400 and neighbor not in visited and neighbor not in obstacles:
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
            if 0 <= neighbor[0] < 560 and 0 <= neighbor[1] < 400 and neighbor not in visited and neighbor not in obstacles:
                stack.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = current

# A* Implementation
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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
            if 0 <= neighbor[0] < 560 and 0 <= neighbor[1] < 400 and neighbor not in obstacles:
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

# Main game loop
while True:
    screen.fill(BLACK)
    draw_grid()
    draw_elements()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Press 'b' to start BFS
                bfs(start_pos, goal_pos)
            elif event.key == pygame.K_d:  # Press 'd' to start DFS
                dfs(start_pos, goal_pos)
            elif event.key == pygame.K_a:  # Press 'a' to start A*
                a_star(start_pos, goal_pos)

    pygame.display.flip()
