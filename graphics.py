# Import pygame library for graphics window
import pygame
import sys

# Initialize pygame
pygame.init()

# Window size
WIDTH = 800
HEIGHT = 600

# Create display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bresenham Line Animation")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# Clock for smooth animation
clock = pygame.time.Clock()

# Initial line coordinates
x1 = 100
y1 = 100
x2 = 200
y2 = 200

# Translation values (movement)
dx_move = 2   # horizontal movement
dy_move = 2   # vertical movement


# -----------------------------------------------------
# BRESENHAM LINE DRAWING ALGORITHM STARTS HERE
# -----------------------------------------------------

def draw_bresenham_line(x1, y1, x2, y2):

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:

        # Plot pixel
        screen.set_at((x1, y1), BLACK)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

# -----------------------------------------------------
# BRESENHAM ALGORITHM ENDS HERE
# -----------------------------------------------------


# Main animation loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Draw line using Bresenham algorithm
    draw_bresenham_line(x1, y1, x2, y2)

    # -------------------------------------------------
    # Translation (movement of the line)
    # -------------------------------------------------

    x1 += dx_move
    x2 += dx_move
    y1 += dy_move
    y2 += dy_move

    # Reverse direction when hitting window boundary
    if x2 >= WIDTH or x1 <= 0:
        dx_move = -dx_move

    if y2 >= HEIGHT or y1 <= 0:
        dy_move = -dy_move

    # Update display
    pygame.display.update()

    # Frame rate for smooth animation
    clock.tick(60)

pygame.quit()
sys.exit()