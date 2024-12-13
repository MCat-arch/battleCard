import pygame
import sys

def show_dashboard(screen):
    pygame.init()
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    # Warna
    BG_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    HOVER_COLOR = (50, 50, 150)

    # Posisi tombol
    buttons = [
        {"text": "Start Game", "pos": (400, 200)},
        {"text": "Settings", "pos": (400, 300)},
        {"text": "Exit", "pos": (400, 400)},
    ]

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            text_surface = font.render(button["text"], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button["pos"])

            # Highlight tombol saat mouse hover
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER_COLOR, text_rect.inflate(20, 10))
            else:
                pygame.draw.rect(screen, BG_COLOR, text_rect.inflate(20, 10))

            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if font.render(button["text"], True, TEXT_COLOR).get_rect(center=button["pos"]).collidepoint(mouse_pos):
                        if button["text"] == "Start Game":
                            return "start_game"
                        elif button["text"] == "Settings":
                            return "settings"
                        elif button["text"] == "Exit":
                            pygame.quit()
                            sys.exit()

        clock.tick(30)
