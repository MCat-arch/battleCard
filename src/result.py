import pygame
import sys

class Result:
    def __init__(self, screen, winner, score):
        self.screen = screen
        self.winner = winner
        self.score = score
        self.font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 30)
        self.background = pygame.image.load("assets/result.png")
        self.button_image = pygame.image.load("assets/back.png")
        self.button_image = pygame.transform.scale(self.button_image, (109, 37))
        self.TEXT_COLOR = (255, 255, 255)
        self.button_rect = pygame.Rect(581, 572, 109, 37)

    def draw_result(self):
        self.screen.blit(self.background, (0, 0))
        winner_text = self.font.render(f"{self.winner} wins!", True, self.TEXT_COLOR)
        score_text = self.font.render(f"{self.score}", True, self.TEXT_COLOR)
        self.screen.blit(winner_text, (600, 341))
        self.screen.blit(score_text, (600, 456))

        self.screen.blit(self.button_image, (581, 572))

        pygame.display.flip()

    def handle_click(self, pos):
        if self.button_rect.collidepoint(pos):
            print("Back button clicked")
            return True
        return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    result = Result(screen, "Player 1", "3 vs 0")

    running = True
    while running:
        result.draw_result()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if result.handle_click(event.pos):
                    running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
