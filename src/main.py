import pygame
from dashboard import Dashboard

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Card Battle Game")
    
    dashboard = Dashboard(screen)
    dashboard.show_dashboard()

    pygame.quit()

if __name__ == "__main__":
    main()

