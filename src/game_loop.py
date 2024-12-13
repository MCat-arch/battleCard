import pygame

def game_loop(screen):
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 100, 0))  # Latar belakang hijau
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)
