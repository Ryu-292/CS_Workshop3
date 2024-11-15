import pygame
import random

class Character:
    def __init__(self, x):
        self.x = x
        self.y = 290
        self.flattened = False
        self.normal_img = pygame.transform.scale(pygame.image.load('opanchu.png'), (90, 110))
        self.flattened_img = pygame.transform.scale(pygame.image.load('opanchu_flat.png'), (100, 30))
        self.img = self.normal_img

    def flatten(self):
        self.flattened = True
        self.img = self.flattened_img
        self.y = 370  # Adjust position for flattened image

    def reset_position(self, x):
        self.flattened = False
        self.img = self.normal_img
        self.x = x  # Reset to the starting position
        self.y = random.choice([250, 290, 330])  # Randomize y position for some variation

    def update(self, screen):
        if self.x >= -100:
            self.x -= 5
        screen.blit(self.img, (self.x, self.y))
