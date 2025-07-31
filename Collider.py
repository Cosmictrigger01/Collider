import pygame
from random import randint
class Enemy:
    def __init__(self):
        self.size = 40
        self.pos = pygame.Vector2(randint(0, screen.get_width()), randint(0, screen.get_height()))
        self.hitbox = pygame.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)
        self.reward = 1
        self.color = "red"
    def draw(self):
        pygame.draw.rect(screen, self.color, self.hitbox, self.size)
    def move_hitbox(self):
        self.hitbox.update(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)


class Player:
    def __init__(self):
        self.size = 40
        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.hitbox = pygame.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)
        self.color = "white"
    def draw(self):
        pygame.draw.rect(screen, self.color, self.hitbox, self.size)
    def move_hitbox(self):
        self.hitbox.update(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)


pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
running = True
menu = True
dt = 0

font = pygame.font.Font(None, 40)
#player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#size = 40
enemies = [Enemy()]
timer = 0
score = 0
selection = 1

while menu:
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            running = False
            menu = False
    
    screen.fill("blue")
    options = {1: "Play",
               2: "Exit"}
    offset = 0
    for num, option in options.items():
        if selection == num:
            text = font.render(option, False, "red")
        else:
            text = font.render(option, False, "white")
        screen.blit(text, (screen.get_width() / 2, screen.get_height() / 2 + offset))
        offset += 100
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if selection > min(options.keys()):
            selection -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if selection < max(options.keys()):
            selection += 1
    if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
        if selection == 1:
            #Creation of player object upon selecting start
            playerObject = Player()
            menu = False
        if selection == 2:
            running = False
            menu = False
    pygame.display.flip()
    clock.tick(60)
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("blue")

    #player_hitbox = pygame.Rect(player_pos.x - size, player_pos.y - size, size * 2, size * 2)
    #pygame.draw.rect(screen, "white", playerObject.hitbox, playerObject.size)
    playerObject.move_hitbox()
    playerObject.draw()
    for e in enemies:
        e.move_hitbox()
        e.draw()
        


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if playerObject.pos.y - 300 * dt - playerObject.size > 0 :
            playerObject.pos.y -= 300 * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if playerObject.pos.y + 300 * dt + playerObject.size < screen.get_height():
            playerObject.pos.y += 300 * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if playerObject.pos.x - 300 * dt - playerObject.size > 0:
            playerObject.pos.x -= 300 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if playerObject.pos.x + 300 * dt + playerObject.size < screen.get_width():
            playerObject.pos.x += 300 * dt

    colliders = []
    for e in enemies:
        if e.hitbox.collidelist([x.hitbox for x in enemies if x.hitbox != e.hitbox]) == -1:
            if e.pos.x > playerObject.pos.x:
                e.pos.x -= 100 * dt
            if e.pos.x < playerObject.pos.x:
                e.pos.x += 100 * dt
            if e.pos.y > playerObject.pos.y:
                e.pos.y -= 100 * dt
            if e.pos.y < playerObject.pos.y:
                e.pos.y += 100 * dt
        else:
            colliders.append(enemies[e.hitbox.collidelist([x.hitbox for x in enemies if x.hitbox != e.hitbox])])
            colliders.append(e)

        if playerObject.hitbox.colliderect(e.hitbox):
            running = False

    for c in colliders:
        if c in enemies:
            score += c.reward
            enemies.remove(c)
            
    text = font.render(f"Score: {score}",False,"white")
    screen.blit(text,(screen.get_width() / 100 * 90, screen.get_height() / 100 * 90))
    pygame.display.flip()
    timer += 1
    if timer % 100 == 0:
        enemies.append(Enemy())
        while enemies[-1].hitbox.colliderect(playerObject.hitbox) or enemies[-1].hitbox.collidelist([x.hitbox for x in enemies if x.hitbox != e.hitbox]) == -1:
            enemies.pop()
            enemies.append(Enemy())
    dt = clock.tick(60) / 1000
pygame.quit()