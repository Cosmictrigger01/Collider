import pygame
import random
screen = pygame.display.set_mode((1920, 1080))

class Buff(pygame.sprite.Sprite):
    def __init__(self, color, pos = None):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = pos
        else:
            self.rect.center = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
    
    def apply(self, player):
        pass

class SpeedBuff(Buff):
    def __init__(self, pos = None):
        super().__init__("green", pos)
    def apply(self, player):
        player.speed_boost(1.75, 2)

class ShrinkBuff(Buff):
    def __init__(self, pos = None):
        super().__init__("yellow", pos)
    def apply(self, player):
        pass