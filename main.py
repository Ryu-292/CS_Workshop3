import pygame
from menu import menu
from game import game
from button import Button
from result import read_player_data, display_leaderboard

pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("OPANCHU TSUBUSHI")

# Load images
background = pygame.transform.scale(pygame.image.load('BG.jpg'), (800, 600))
background1 = pygame.transform.scale(pygame.image.load('BG1.png'), (800, 600))
gameover = pygame.transform.scale(pygame.image.load('GO.png'), (400, 500))

# # Menu screen
# player_name, start_time = menu(screen)

# # Start the game after the menu
# game(screen, background, background1, gameover, player_name, start_time)

# Game loop with restart logic
while True:
    player_name, start_time = menu(screen)
    restart = game(screen, background, background1, gameover, player_name, start_time)
    if not restart:
        break

