forest_map = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
]

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
TILE_SIZE = 50
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon Forest")

# Load and resize player and NPC character images
player_image = pygame.image.load("player.png")  # Replace with your player image
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))

npc_image_up = pygame.image.load("npc_up.png")  # Replace with your NPC image facing up
npc_image_up = pygame.transform.scale(npc_image_up, (TILE_SIZE, TILE_SIZE))

# Set initial player position
player_x, player_y = 2, 2

# Set initial NPC position and state
npc_x, npc_y = 6, 6
npc_directions = ["up", "down", "left", "right"]
npc_direction = "up"
npc_last_change_time = pygame.time.get_ticks()
npc_change_interval = 5000  # Change direction every 5 seconds
npc_engage_distance = 3  # Adjust the distance at which NPC engages the player

# Flag to check if the battle is initiated
battle_initiated = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(10)  # Adjust the speed of the game

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    next_x, next_y = player_x, player_y

    if keys[pygame.K_LEFT]:
        next_x -= 1
    elif keys[pygame.K_RIGHT]:
        next_x += 1
    elif keys[pygame.K_UP]:
        next_y -= 1
    elif keys[pygame.K_DOWN]:
        next_y += 1

    # Check if the next position is valid (not occupied by the NPC or a tree)
    if forest_map[next_y][next_x] == 0 and (next_x != npc_x or next_y != npc_y):
        player_x, player_y = next_x, next_y

    # NPC behavior - Change direction every 5 seconds
    current_time = pygame.time.get_ticks()
    if current_time - npc_last_change_time >= npc_change_interval:
        npc_last_change_time = current_time
        npc_direction = npc_directions[(npc_directions.index(npc_direction) + 1) % len(npc_directions)]

    if not battle_initiated:
        if npc_x == player_x:
            if npc_y < player_y:
                npc_direction = "down"
            elif npc_y > player_y:
                npc_direction = "up"
        elif npc_y == player_y:
            if npc_x < player_x:
                npc_direction = "right"
            elif npc_x > player_x:
                npc_direction = "left"

        if npc_x - npc_engage_distance <= player_x <= npc_x + npc_engage_distance \
                and npc_y - npc_engage_distance <= player_y <= npc_y + npc_engage_distance:
            battle_initiated = True

    # Draw background
    screen.fill(WHITE)

    # Draw forest map
    for y, row in enumerate(forest_map):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player character
    screen.blit(player_image, (player_x * TILE_SIZE, player_y * TILE_SIZE))

    # Draw NPC character
    if npc_direction == "up":
        screen.blit(npc_image_up, (npc_x * TILE_SIZE, npc_y * TILE_SIZE))
    # Add similar conditions for other directions

    # Draw battle initiation indicator around NPC
    if battle_initiated:
        pygame.draw.circle(screen, RED, (npc_x * TILE_SIZE + TILE_SIZE // 2, npc_y * TILE_SIZE + TILE_SIZE // 2),
                           TILE_SIZE * npc_engage_distance, 2)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
