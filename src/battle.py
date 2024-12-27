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
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180

        # State
        self.selected_card = None
        self.opponent_card = None
        self.current_player = player1

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
            for i, card in enumerate(self.player1.cards):
                self.draw_card(card, (100 + i * (self.CARD_WIDTH + 10), 200))

        # Gambar kartu utama player 2
        if self.player2.cards:
            for i, card in enumerate(self.player2.cards):
                self.draw_card(card, (500 + i * (self.CARD_WIDTH + 10), 200))

        pygame.display.flip()

    def handle_click(self, pos):
        """Tangani klik mouse untuk memilih kartu."""
        if self.current_player == self.player1:
            for i, card in enumerate(self.player1.cards):
                card_rect = pygame.Rect(100 + i * (self.CARD_WIDTH + 10), 200, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    self.selected_card = card
                    print(f"Player 1 selected {card.name}")
                    return
        else:
            for i, card in enumerate(self.player2.cards):
                card_rect = pygame.Rect(500 + i * (self.CARD_WIDTH + 10), 200, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    self.selected_card = card
                    print(f"Player 2 selected {card.name}")
                    return

        if self.selected_card:
            if self.current_player == self.player1:
                for i, card in enumerate(self.player2.cards):
                    card_rect = pygame.Rect(500 + i * (self.CARD_WIDTH + 10), 200, self.CARD_WIDTH, self.CARD_HEIGHT)
                    if card_rect.collidepoint(pos):
                        self.opponent_card = card
                        print(f"Player 1 selected {card.name} as opponent")
                        self.battle_cards()
                        return
            else:
                for i, card in enumerate(self.player1.cards):
                    card_rect = pygame.Rect(100 + i * (self.CARD_WIDTH + 10), 200, self.CARD_WIDTH, self.CARD_HEIGHT)
                    if card_rect.collidepoint(pos):
                        self.opponent_card = card
                        print(f"Player 2 selected {card.name} as opponent")
                        self.battle_cards()
                        return

    def battle_cards(self):
        """Lakukan battle antara dua kartu yang dipilih."""
        if self.selected_card and self.opponent_card:
            self.animate_attack((260, 290), (540, 290))
            self.opponent_card.hp -= self.selected_card.atk
            if self.opponent_card.hp <= 0:
                print(f"{self.opponent_card.name} is defeated!")
                if self.current_player == self.player1:
                    self.player2.cards.remove(self.opponent_card)
                else:
                    self.player1.cards.remove(self.opponent_card)

            self.selected_card, self.opponent_card = None, None
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def start_battle(self):
        """Mulai battle antara dua kartu utama."""
        running = True
        while running:
            self.draw_battlefield()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Check if any player has no cards left
            if not self.player1.cards or not self.player2.cards:
                running = False

            self.clock.tick(30)

        # Display the result
        self.display_result()

    def display_result(self):
        """Tampilkan hasil battle."""
        self.screen.blit(self.background, (0, 0))
        if not self.player1.cards:
            result_text = "Player 2 wins!"
        elif not self.player2.cards:
            result_text = "Player 1 wins!"
        else:
            result_text = "It's a draw!"
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