import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((560, 400))
pygame.display.set_caption("Pygame Maze Solver")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to draw grid
def draw_grid():
    for x in range(0, 560, 20):  # 28 columns
        for y in range(0, 400, 20):  # 20 rows
            rect = pygame.Rect(x, y, 20, 20)
            pygame.draw.rect(screen, WHITE, rect, 1)  # 1 means border thickness

# Main game loop
while True:
    screen.fill(BLACK)
    draw_grid()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update the display
    pygame.display.flip()

    START_COLOR = (0, 0, 255)
    GOAL_COLOR = (255, 0, 0)
    ROBOT_COLOR = (0, 255, 0)
    OBSTACLE_COLOR = (169, 169, 169)

    start_pos = (0, 0)  # Top-left corner
    goal_pos = (540, 380)  # Bottom-right corner

    def draw_elements():
        # Draw Start
        pygame.draw.rect(screen, START_COLOR, (start_pos[0], start_pos[1], 20, 20))
        # Draw Goal
        pygame.draw.rect(screen, GOAL_COLOR, (goal_pos[0], goal_pos[1], 20, 20))

    # Main game loop (continued)
    while True:
        screen.fill(BLACK)
        draw_grid()
        draw_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

        obstacles = [(100, 100), (120, 140), (180, 200)]  # Example positions

        def draw_elements():
            # Draw Start
            pygame.draw.rect(screen, START_COLOR, (start_pos[0], start_pos[1], 20, 20))
            # Draw Goal
            pygame.draw.rect(screen, GOAL_COLOR, (goal_pos[0], goal_pos[1], 20, 20))
            # Draw Obstacles
            for obs in obstacles:
                pygame.draw.rect(screen, OBSTACLE_COLOR, (obs[0], obs[1], 20, 20))
        