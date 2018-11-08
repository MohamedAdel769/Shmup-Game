from setting import *
import  sys
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(Title)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(path.join(font_dir, font_name), size)
    text_surf = font.render(text, True, YELLOW)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surf, text_rect)


def newEnemy():
    enem = Enemy()
    enemies.add(enem)
    all_sprites.add(enem)


def draw_Health_bar(surf, x, y, percentage):
    if percentage < 0:
        percentage = 0
    fill = (percentage / 100) * BAR_LENGTH
    border_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, border_rect, 2)


def draw_lives(surf, imag, x, y, lives):
    for life in range(lives):
        img_rect = imag.get_rect()
        img_rect.x = x + 30 * life
        img_rect.y = y
        surf.blit(imag, img_rect)


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
        self.Health = HEALTH
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.last_hide = pygame.time.get_ticks()
        self.pow_level = 1
        self.pow_upd = pygame.time.get_ticks()

    def update(self):
        if self.pow_level >= 2 and pygame.time.get_ticks() - self.pow_upd > POWER_UP_TIME:
            self.pow_level -= 1
            self.pow_upd = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if self.hidden and now - self.last_hide > 1350:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedX = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedX -= 8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedX += 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedX
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.pow_level == 1:
                b = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(b)
                bullets.add(b)
            elif self.pow_level >= 2:
                b1 = Bullet(self.rect.left, self.rect.centery)
                b2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(b1)
                all_sprites.add(b2)
                bullets.add(b1)
                bullets.add(b2)
            shoot_snd.play()

    def hide(self):
        self.hidden = True
        self.last_hide = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 300)

    def powerUp(self):
        self.pow_level += 1
        self.pow_upd = pygame.time.get_ticks()


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


class Explosions(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_img[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 70
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_img[self.size]):
                self.kill()
            else:
                old_center = self.rect.center
                self.image = explosion_img[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = old_center


class PowerUps(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'bolt'])
        self.image = pow_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


def Show_menu():
    screen.blit(BG2, BG2_rect)
    draw_text(screen, "SHMUP!", 55, WIDTH / 2, HEIGHT / 5)
    draw_text(screen, "Arrow Keys to Move, Space to Shoot", 14, WIDTH / 2, HEIGHT / 2 - 40)
    draw_text(screen, "Press any key to START", 15, WIDTH / 2, HEIGHT / 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(loops=-1)

# Load all graphics
pow_img = {}
pow_img['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
pow_img['bolt'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
shield_img = pygame.image.load(path.join(img_dir, 'spr_shield.png')).convert()
BG = pygame.image.load(path.join(img_dir, "bg.png")).convert()
BG_rect = BG.get_rect()
BG2 = pygame.image.load(path.join(img_dir, "rsz_bg3.png")).convert()
BG2_rect = BG2.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
player_Mini_img = pygame.transform.scale(player_img, (25, 19))
player_Mini_img.set_colorkey(BLACK)
laser_img = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()
meteor_imgs = []
meteor_list = ['meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_small1.png',
               'meteorBrown_tiny1.png', 'meteorGrey_big3.png', 'meteorGrey_med2.png',
               'meteorGrey_small2.png', 'meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_imgs.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_img = {}
explosion_img['large'] = []
explosion_img['small'] = []
explosion_img['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    sm_img = pygame.transform.scale(img, (32, 32))
    lg_img = pygame.transform.scale(img, (70, 70))
    explosion_img['large'].append(lg_img)
    explosion_img['small'].append(sm_img)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_img['player'].append(img)


# Load all sounds
shoot_snd = pygame.mixer.Sound(path.join(snd_dir, 'Hit_Hurt8.wav'))
pow_S_snd = pygame.mixer.Sound(path.join(snd_dir, 'shield_pow.wav'))
pow_B_snd = pygame.mixer.Sound(path.join(snd_dir, 'bolt_pow.wav'))
exp_snd = pygame.mixer.Sound(path.join(snd_dir, 'Hit_Hurt105.wav'))
death_snd = pygame.mixer.Sound(path.join(snd_dir, 'death_snd.ogg'))
exp_snd.set_volume(0.1)
expl_snd = []
expl_snd.append(pygame.mixer.Sound(path.join(snd_dir, 'Explosion4.wav')))
expl_snd.append(pygame.mixer.Sound(path.join(snd_dir, 'Explosion3.wav')))
pygame.mixer.music.load(path.join(snd_dir, 'e.ogg'))
pygame.mixer.music.set_volume(0.5)


pygame.mixer.music.play(loops=-1)
# Game loop
running = True
game_over = True
while running:
    if game_over:
        Show_menu()
        game_over = False
        score = 0
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newEnemy()

    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collision
    # bullet hit an enemy
    Bhits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in Bhits:
        if hit.radius > 15:
            score += 5
        else:
            score += 10
        random.choice(expl_snd).play()
        Exp = Explosions(hit.rect.center, 'large')
        all_sprites.add(Exp)
        if random.random() > 0.91:
            pow = PowerUps(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newEnemy()
    # enemy hit the player
    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.Health -= hit.radius
        Exp = Explosions(hit.rect.center, 'small')
        all_sprites.add(Exp)
        exp_snd.play()
        newEnemy()
        if player.Health <= 0:
            death_snd.play()
            expl = Explosions(player.rect.center, 'player')
            all_sprites.add(expl)
            player.hide()
            player.Health = 100
            player.lives -= 1
    if player.lives == 0 and not expl.alive():
        game_over = True

    # player take a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.Health = (player.Health + 15)
            if player.Health > 100:
                player.Health = 100
            pow_S_snd.play()
        elif hit.type == 'bolt':
            player.powerUp()
            pow_B_snd.play()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(BG, BG_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_Health_bar(screen, 5, 5, player.Health)
    draw_lives(screen, player_Mini_img, WIDTH - 100, 5, player.lives)
    # flip the display
    pygame.display.flip()

pygame.quit()
