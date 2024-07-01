import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Square")

# Set up the square
square_size = 50
square_color = (255, 0, 0)  # Red color
square_x = screen_width // 2
square_y = screen_height // 2
square_speed = 5

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move the square
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
    if keys[pygame.K_UP]:
        square_y -= square_speed
    if keys[pygame.K_DOWN]:
        square_y += square_speed

    # Keep the square within screen boundaries
    if square_x < 0:
        square_x = 0
    if square_x > screen_width - square_size:
        square_x = screen_width - square_size
    if square_y < 0:
        square_y = 0
    if square_y > screen_height - square_size:
        square_y = screen_height - square_size

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw the square
    pygame.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
