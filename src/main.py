import pygame
from dashboard import show_dashboard
from game_loop import game_loop

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battle Card Game")

    while True:
        result = show_dashboard(screen)

        if result == "start_game":
            game_loop(screen)
        elif result == "settings":
            print("Settings menu not implemented yet.")
        elif result == "exit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
