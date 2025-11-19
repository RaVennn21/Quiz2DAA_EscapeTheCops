
import pygame
import sys
import random
from maze_generator import Maze
from core import Player,Police

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 20
MAZE_WIDTH = 21
MAZE_HEIGHT = 11
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 120, 200)
GREEN = (50, 200, 50)
DARK_GRAY = (60, 60, 60)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game - Find the Exit!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# Generate maze
maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
maze.create_maze(1, 1)
maze.set_random_exit()
Maze.add_loops(maze, loop_count=10)

# Create player
player = Player(maze, CELL_SIZE)
police = Police(maze, maze.width - 2, maze.height - 2)


def draw_maze():
    """Draw the maze on the screen"""
    for y in range(maze.height):
        for x in range(maze.width):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if maze.is_wall(x, y):
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

            if maze.exit and (x, y) == maze.exit:
                pygame.draw.rect(screen, GREEN, rect)

def draw_ui():
    """Draw the UI elements"""
    ui_y = MAZE_HEIGHT * CELL_SIZE
    pygame.draw.rect(screen, DARK_GRAY, (0, ui_y, SCREEN_WIDTH, 50))
    text = font.render(f"Moves: {player.moves} | Arrow Keys/WASD to move", True, WHITE)
    screen.blit(text, (10, ui_y + 15))

# Main game loop
running = True
while running:
    clock.tick(5)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player
    player.update()
    police.update(player)
    

    # Drawing
    screen.fill(WHITE)
    draw_maze()
    player.draw(screen)
    police.draw(screen, CELL_SIZE)
    draw_ui()

    # Draw victory message
    if player.game_won:
        victory_text = font.render(f"YOU WON in {player.moves} moves! Press ESC to exit",True, GREEN)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
    if player.game_lost:
        lost_text = font.render("YOU LOST! Caught by the police! Press ESC to exit", True, (255, 0, 0))
        screen.blit(lost_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()