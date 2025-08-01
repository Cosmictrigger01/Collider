import pygame
import random
import pickle
class Enemy:
    def __init__(self):
        self.size = 40
        self.pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
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

    def playerMovement(self, dt):
        # global keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.pos.y - 300 * dt - self.size > 0:
                self.pos.y -= 300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.pos.y + 300 * dt + self.size < screen.get_height():
                self.pos.y += 300 * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.pos.x - 300 * dt - self.size > 0:
                self.pos.x -= 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.pos.x + 300 * dt + self.size < screen.get_width():
                self.pos.x += 300 * dt


class Player2(pygame.sprite.Sprite):
    def __init__(self, color, buff_group):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = 5

        self.buff_group = buff_group
    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.velocity
    def check_collisions(self):
        if pygame.sprite.spritecollide(self, buff_group, True):
            # Handle collision with buffs
            print("Buff collected!")
            # Here you can add logic to increase score or apply buffs






class Buff(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        self.velocity = 0

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top > screen.get_height():
            self.kill()


class Progress():
    def __init__(self):
        self.points = 0
        self.unlocks = []

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# Create a sprite group for buffs
buff_group = pygame.sprite.Group()
for i in range(10):  # Create 10 green buffs
    buff_green = Buff("green")
    buff_group.add(buff_green)

# Create player group
player2 = Player2("black", buff_group)
player_group = pygame.sprite.Group()
player_group.add(player2)

def load():
    try:
        with open("progress.pkl", "rb") as infile:
            progress = pickle.load(infile)
            return progress
    except:
        progress = Progress()
        return progress

def save(progress):
    with open("progress.pkl", "wb") as outfile:
        pickle.dump(progress, outfile)

def play(clock):
    running = True
    playerObject = Player()
    enemies = [Enemy()]
    timer = 0
    score = 0
    dt = 0
    font = pygame.font.Font(None, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("blue")


        playerObject.move_hitbox()
        playerObject.draw()

        # Draw and move buffs
        buff_group.update()
        buff_group.draw(screen)

        # Draw and move player
        player_group.update()
        player_group.draw(screen)

        for e in enemies:
            e.move_hitbox()
            e.draw()

        playerObject.playerMovement(dt)

        colliders = []
        for e in enemies:
            if coll := e.hitbox.collidelist([x.hitbox for x in enemies if x.hitbox != e.hitbox]) == -1:
                if e.pos.x > playerObject.pos.x:
                    e.pos.x -= 100 * dt
                if e.pos.x < playerObject.pos.x:
                    e.pos.x += 100 * dt
                if e.pos.y > playerObject.pos.y:
                    e.pos.y -= 100 * dt
                if e.pos.y < playerObject.pos.y:
                    e.pos.y += 100 * dt
            else:
                colliders.append(enemies[coll])
                colliders.append(e)

            if playerObject.hitbox.colliderect(e.hitbox):
                running = False

        for c in colliders:
            if c in enemies:
                score += c.reward
                enemies.remove(c)

        text = font.render(f"Score: {score}", False, "white")
        screen.blit(text, (screen.get_width() / 100 * 90, screen.get_height() / 100 * 90))
        pygame.display.flip()
        timer += 1
        if timer % 100 == 0:
            enemies.append(Enemy())
            while enemies[-1].hitbox.colliderect(playerObject.hitbox) or enemies[-1].hitbox.collidelist(
                    [x.hitbox for x in enemies if x.hitbox != e.hitbox]) == -1:
                enemies.pop()
                enemies.append(Enemy())
        dt = clock.tick(60) / 1000
    return score

def menu(progress, clock):
    menu = True
    running = True
    selection = 1
    font = pygame.font.Font(None, 40)
    while menu:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                return

        screen.fill("blue")
        options = {1: "Play",
                   2: "Exit",
                   3: f"Points: {progress.points}"}
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
                # Creation of player object upon selecting start
                score = play(clock)
                progress.points += score
            if selection == 2:
                save(progress)
                return
        pygame.display.flip()
        clock.tick(60)

menu(load(), clock)
pygame.quit()