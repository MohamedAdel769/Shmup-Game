from setting import *

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(Title)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedX = 0

    def update(self):
        self.speedX = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedX -= 8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedX += 8
        self.rect.x += self.speedX
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        b = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(b)
        bullets.add(b)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(3, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -35 or self.rect.right > WIDTH + 35:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(3, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    enem = Enemy()
    enemies.add(enem)
    all_sprites.add(enem)
# Game loop
running = True
while running:
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check for collision
    Bhits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in Bhits:
        enem = Enemy()
        enemies.add(enem)
        all_sprites.add(enem)
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # flip the display
    pygame.display.flip()

pygame.quit()
