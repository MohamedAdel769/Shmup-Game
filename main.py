from setting import *

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(Title)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Game loop
running = True
while running:
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # flip the display
    pygame.display.flip()

pygame.quit()
