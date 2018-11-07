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
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
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
        self.orig_image = random.choice(meteor_imgs)
        self.orig_image.set_colorkey(BLACK)
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(3, 8)
        self.rotation = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_rot = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_rot > 50:
            self.last_rot = now
            self.rotation = (self.rotation + self.rot_speed) % 360
            new_img = pygame.transform.rotate(self.orig_image, self.rotation)
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
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
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()


# Load all graphics
BG = pygame.image.load(path.join(img_dir, "bg.png")).convert()
BG_rect = BG.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()
meteor_imgs = []
meteor_list = ['meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_small1.png',
               'meteorBrown_tiny1.png', 'meteorGrey_big3.png', 'meteorGrey_med2.png',
               'meteorGrey_small2.png', 'meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_imgs.append(pygame.image.load(path.join(img_dir, img)).convert())

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
    hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(BG, BG_rect)
    all_sprites.draw(screen)
    # flip the display
    pygame.display.flip()

pygame.quit()
