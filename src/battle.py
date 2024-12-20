import pygame
import sys
from card import Card

class Battle:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        self.player1 = player1
        self.player2 = player2
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load("assets/battlefield.png")

        # Warna
        self.TEXT_COLOR = (255, 255, 255)
        self.CARD_COLOR = (100, 100, 250)
        self.ATTACK_COLOR = (255, 0, 0)

        # Ukuran kartu
        self.CARD_WIDTH = 101
        self.CARD_HEIGHT = 112

    def draw_card(self, card, pos, color=None):
        """Gambar kartu di layar."""
        card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)

        # Tampilkan informasi kartu
        name_text = self.font.render(card.name, True, self.TEXT_COLOR)
        self.screen.blit(name_text, (pos[0] + 10, pos[1] + 10))

        hp_text = self.font.render(f"HP: {card.hp}", True, self.TEXT_COLOR)
        self.screen.blit(hp_text, (pos[0] + 10, pos[1] + 50))

        atk_text = self.font.render(f"ATK: {card.atk}", True, self.TEXT_COLOR)
        self.screen.blit(atk_text, (pos[0] + 10, pos[1] + 90))

    def animate_attack(self, attacker_pos, defender_pos):
        """Animasi serangan."""
        for _ in range(10):
            pygame.draw.line(self.screen, self.ATTACK_COLOR, attacker_pos, defender_pos, 5)
            pygame.display.flip()
            self.clock.tick(30)
            self.screen.blit(self.background, (0, 0))
            self.draw_battlefield()

    def draw_battlefield(self):
        """Gambar battlefield di layar."""
        self.screen.blit(self.background, (0, 0))

        # Gambar kartu utama player 1
        if self.player1.cards:
            main_card1 = self.player1.cards[0]
            self.draw_card(main_card1, (275, 258))

        # Gambar kartu utama player 2
        if self.player2.cards:
            main_card2 = self.player2.cards[0]
            self.draw_card(main_card2, (456, 258))

        pygame.display.flip()

    def start_battle(self):
        """Mulai battle antara dua kartu utama."""
        running = True
        while running:
            self.draw_battlefield()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Battle logic
            main_card1 = self.player1.cards[0]
            main_card2 = self.player2.cards[0]

            # Player 1 attacks
            self.animate_attack((260, 290), (540, 290))
            main_card2.hp -= main_card1.atk
            if main_card2.hp <= 0:
                print(f"{main_card2.name} is defeated!")
                running = False
                break

            # Player 2 attacks
            self.animate_attack((540, 290), (260, 290))
            main_card1.hp -= main_card2.atk
            if main_card1.hp <= 0:
                print(f"{main_card1.name} is defeated!")
                running = False
                break

            self.clock.tick(1)  # Slow down the battle for better visualization

        # Display the result
        self.display_result(main_card1, main_card2)

    def display_result(self, card1, card2):
        """Tampilkan hasil battle."""
        self.screen.blit(self.background, (0, 0))
        result_text = f"{card1.name} wins!" if card2.hp <= 0 else f"{card2.name} wins!"
        result_surface = self.font.render(result_text, True, self.TEXT_COLOR)
        self.screen.blit(result_surface, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing

# Contoh penggunaan
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battle Example")

    class Player:
        def __init__(self, name):
            self.name = name
            self.cards = []

        def add_card(self, card):
            self.cards.append(card)

    player1 = Player("Player 1")
    player1.add_card(Card("Dragon", 100, 20, 50))

    player2 = Player("Player 2")
    player2.add_card(Card("Phoenix", 80, 25, 60))

    battle = Battle(screen, player1, player2)
    battle.start_battle()