import pygame
screen = pygame.display.set_mode((1920, 1080))

class Player(pygame.sprite.Sprite):
    def __init__(self, progress: "Progress", color, buff_group):
        super().__init__()
        self.size = progress.size
        self.base_size = progress.size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = progress.velocity
        self.base_velocity = progress.velocity
        self.score = 0
        self.speed_boost_timer = 0
        self.buff_group = buff_group

    def update(self, dt):
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.velocity = self.base_velocity

        self.move(dt)
        self.check_collisions()

    def speed_boost(self, increase, duration):
        if self.speed_boost_timer > 0:
            self.speed_boost_timer += duration
        else:
            self.velocity *= increase
            self.speed_boost_timer += duration

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if (self.rect.x) - self.velocity * dt > 0:
                self.rect.x -= self.velocity * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if (self.rect.x + self.size) + self.velocity * dt < screen.get_width():
                self.rect.x += self.velocity * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if (self.rect.y) - self.velocity * dt > 0:
                self.rect.y -= self.velocity * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if (self.rect.y + self.size) + self.velocity * dt < screen.get_height():
                self.rect.y += self.velocity * dt

    # Handle collision with buffs
    def check_collisions(self):
        buff_list = pygame.sprite.spritecollide(self, self.buff_group, True)
        for i in buff_list:
            i.apply(self)
           