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

class Player(pygame.sprite.Sprite):
    def __init__(self, progress: "Progress", color, buff_group):
        super().__init__()
        self.size = progress.size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = progress.velocity
        self.score = 0

        self.buff_group = buff_group
    def update(self, dt):
        self.move(dt)
        self.check_collisions()

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

    def check_collisions(self):
        if pygame.sprite.spritecollide(self, self.buff_group, True):
            # Handle collision with buffs
            print("Buff collected!")
            # Here you can add logic to increase score or apply buffs
            self.score += 1

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
        self.size = 80
        self.size_level = 0
        self.velocity = 300
        self.vel_level = 0

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()


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

def play(progress, clock):
    running = True
    enemies = [Enemy()]
    enemy_spawn_rate = 100 # lower is faster
    timer = 0
    dt = 0
    font = pygame.font.Font(None, 40)

    # Create a sprite group for buffs
    buff_group = pygame.sprite.Group()
    for i in range(10):  # Create 10 green buffs
        buff_green = Buff("green")
        buff_group.add(buff_green)

    # Create player group
    player = Player(progress, "black", buff_group)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("blue")

        # Draw and move buffs
        buff_group.update()
        buff_group.draw(screen)

        # Draw and move player
        player_group.update(dt)
        player_group.draw(screen)

        for e in enemies:
            e.move_hitbox()
            e.draw()

        colliders = []
        for e in enemies:
            coll_index = e.hitbox.collidelist([x.hitbox for x in enemies if x.hitbox != e.hitbox])
            if  coll_index == -1:
                if e.pos.x > player.rect.x + player.size / 2:
                    e.pos.x -= 100 * dt
                if e.pos.x < player.rect.x + player.size / 2:
                    e.pos.x += 100 * dt
                if e.pos.y > player.rect.y + player.size / 2:
                    e.pos.y -= 100 * dt
                if e.pos.y < player.rect.y + player.size / 2:
                    e.pos.y += 100 * dt
            else:
                if enemies.index(e) < enemies.index(enemies[coll_index]):
                    colliders.append(enemies[coll_index + 1])
                else:
                    colliders.append(enemies[coll_index])
                colliders.append(e)

            if player.rect.colliderect(e.hitbox):
                running = False

        for c in colliders:
            if c in enemies:
                player.score += c.reward
                enemies.remove(c)

        text = font.render(f"Score: {player.score}", False, "white")
        screen.blit(text, (screen.get_width() / 100 * 90, screen.get_height() / 100 * 90))
        pygame.display.flip()
        timer += 1
        if timer % enemy_spawn_rate == 0:
            enemies.append(Enemy())
            while enemies[-1].hitbox.colliderect(player.rect) or enemies[-1].hitbox.collidelist(
                    [x.hitbox for x in enemies if x.hitbox != e.hitbox]) == -1:
                enemies.pop()
                enemies.append(Enemy())
            if player.score % 5 == 0 and enemy_spawn_rate > 10:
                enemy_spawn_rate -= 1

        dt = clock.tick(60) / 1000
    return player.score

def upgrades(progress: "Progress", clock):
    upgrades_menu = True
    selection = 1
    font = pygame.font.Font(None, 40)
    while upgrades_menu:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                return

        screen.fill("blue")

        options = {1: {"text": "Reduce Size",
                       "cost": 100,
                       "change": 10,
                       "max_level": 5},
                   2: {"text": "Increase Speed",
                       "cost": 100,
                       "change": 25,
                       "max_level": 5},
                   3: "Exit",
                   4: f"Points: {progress.points}"}
        
        offset = 0
        for num, option in options.items():
            if selection == num and num <= 2:
                print(option)
                text = font.render(f"{option['text']} by {option['change']}, Current Level: {progress.size_level}(Max: {option['max_level']}), Cost: {option['cost']}", False, "red")
            elif selection != num and num <= 2:
                print(option)
                text = font.render(f"{option['text']} by {option['change']}, Current Level: {progress.vel_level}(Max: {option['max_level']}), Cost: {option['cost']}", False, "white")
            if selection == num and num > 2:
                text = font.render(option, False, "red")
            elif selection != num and num > 2:
                text = font.render(option, False, "white")

            screen.blit(text, (screen.get_width() / 2, screen.get_height() / 2 + offset))
            offset += 100

        keys = pygame.key.get_just_released()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if selection > min(options.keys()):
                selection -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if selection < max(options.keys()):
                selection += 1
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if selection == 1:
                if progress.size_level < 5 and progress.points > options[selection]["cost"]:
                    progress.size -= options[selection]["change"]
                    progress.points -= options[selection]["cost"]
                    progress.size_level += 1
            if selection == 2:
                if progress.vel_level < 5 and progress.points > options[selection]["cost"]:
                    progress.velocity += options[selection]["change"]
                    progress.points -= options[selection]["cost"]
                    progress.vel_level += 1
            if selection == 3:
                return progress
        pygame.display.flip()
        clock.tick(60)

def menu(progress, clock):
    menu = True
    selection = 1
    font = pygame.font.Font(None, 40)
    while menu:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                save(progress)
                return

        screen.fill("blue")

        options = {1: "Play",
                   2: "Upgrades",
                   3: "Exit",
                   4: f"Points: {progress.points}"}
        
        offset = 0
        for num, option in options.items():
            if selection == num:
                text = font.render(option, False, "red")
            else:
                text = font.render(option, False, "white")

            screen.blit(text, (screen.get_width() / 2, screen.get_height() / 2 + offset))
            offset += 100

        keys = pygame.key.get_just_released()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if selection > min(options.keys()):
                selection -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if selection < max(options.keys()):
                selection += 1
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if selection == 1:
                score = play(progress, clock)
                progress.points += score
            if selection == 2:
                progress = upgrades(progress, clock)
                selection = 1
            if selection == 3:
                save(progress)
                return
            
        pygame.display.flip()
        clock.tick(60)

menu(load(), clock)
pygame.quit()