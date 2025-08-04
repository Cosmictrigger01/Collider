import pygame
import random


class Enemy:
    def __init__(self, screen):
        self.screen = screen
        self.size = 40
        self.pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        self.hitbox = pygame.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)
        self.reward = 1
        self.color = "red"

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.hitbox, self.size)

    def move_hitbox(self):
        self.hitbox.update(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)
 