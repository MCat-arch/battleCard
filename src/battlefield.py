import pygame
import sys
from shop import Shop
from card import Card
from battle import Battle

class Battlefield:
    def __init__(self, screen, players):
        self.screen = screen
        self.players = players
        self.current_player_idx = 0
        self.turns_taken = 0
        self.rounds = 0
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

        # Warna
        self.BG_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (255, 255, 255)
        self.CARD_COLOR = (100, 100, 250)
        self.DECK_COLOR = (250, 100, 100)
        self.BUTTON_COLOR = (100, 255, 100)

        # Ukuran kartu
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180

        # Menyiapkan Shop
        self.shop = None
        self.shop_active = False
        self.shop_cards = []

        # Timer
        self.turn_time = 20  # 20 seconds per turn
        self.turn_start_time = pygame.time.get_ticks()

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

    def draw_battlefield(self):
        """Gambar battlefield di layar."""
        self.screen.fill(self.BG_COLOR)

        # Gambar kartu utama
        current_player = self.players[self.current_player_idx]
        if current_player.cards:
            main_card = current_player.cards[0]
            self.draw_card(main_card, (340, 100))

        # Gambar kartu tambahan
        if len(current_player.cards) > 1:
            start_x = 200
            gap = 20
            for i, card in enumerate(current_player.cards[1:], start=1):
                x = start_x + (self.CARD_WIDTH + gap) * (i - 1)
                y = 300
                self.draw_card(card, (x, y))

        # Gambar deck kartu hasil shop
        if self.shop_cards:
            start_x = 340
            for i, card in enumerate(self.shop_cards):
                x = start_x + (self.CARD_WIDTH + 10) * i
                y = 500
                self.draw_card(card, (x, y), self.DECK_COLOR)

        # Gambar tombol Merge dan Shop
        self.draw_buttons()

        # Gambar timer
        elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000
        remaining_time = max(0, self.turn_time - elapsed_time)
        timer_text = f"Time left: {int(remaining_time)}s"
        timer_surface = self.font.render(timer_text, True, self.TEXT_COLOR)
        self.screen.blit(timer_surface, (340, 50))

        pygame.display.flip()

        # Check if time is up
        if remaining_time <= 0:
            self.switch_turn()

    def draw_buttons(self):
        """Gambar tombol Merge dan Shop."""
        # Tombol Merge
        merge_button = pygame.Rect(50, 500, 100, 40)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, merge_button)
        merge_text = self.font.render("Merge", True, self.TEXT_COLOR)
        self.screen.blit(merge_text, (merge_button.x + 10, merge_button.y + 5))

        # Tombol Shop
        shop_button = pygame.Rect(650, 500, 100, 40)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, shop_button)
        shop_text = self.font.render("Shop", True, self.TEXT_COLOR)
        self.screen.blit(shop_text, (shop_button.x + 15, shop_button.y + 5))

    def handle_click(self, pos):
        """Tangani klik mouse."""
        merge_button = pygame.Rect(50, 500, 100, 40)
        shop_button = pygame.Rect(650, 500, 100, 40)

        if merge_button.collidepoint(pos):
            print("Merge clicked")
            self.merge_card()

        if shop_button.collidepoint(pos):
            print("Shop clicked")
            self.open_shop()

    def swap_card(self, index):
        """Swap kartu utama dengan kartu lain."""
        current_player = self.players[self.current_player_idx]
        if index < len(current_player.cards):
            current_player.cards[0], current_player.cards[index] = (
                current_player.cards[index],
                current_player.cards[0],
            )
            print(f"Swapped main card with card at index {index}")

    def merge_card(self):
        """Merge kartu utama dengan kartu dari deck shop."""
        current_player = self.players[self.current_player_idx]
        if self.shop_cards:
            main_card = current_player.cards[0]
            shop_card = self.shop_cards.pop(0)  # Ambil kartu pertama di shop

            # Gabungkan atribut kartu
            merged_card = Card(
                name=f"{main_card.name}+{shop_card.name}",
                hp=main_card.hp + shop_card.hp,
                atk=main_card.atk + shop_card.atk,
                price=(main_card.price + shop_card.price) // 2,
            )
            current_player.cards[0] = merged_card
            print(f"Merged cards into: {merged_card.name}")

    def open_shop(self):
        """Buka shop untuk menambahkan kartu ke deck shop."""
        self.shop_active = True
        self.shop = Shop(self.screen, self.players[self.current_player_idx])
        new_card = Card("ShopCard", 50, 10, 20)  # Contoh kartu shop
        self.shop_cards.append(new_card)
        print("Added new card from shop")

    def switch_turn(self):
        """Switch to the next player's turn."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.turn_start_time = pygame.time.get_ticks()
        self.turns_taken += 1

        # Check if both players have had their turn
        if self.turns_taken >= len(self.players):
            self.turns_taken = 0
            self.rounds += 1
            self.start_battle()

    def start_battle(self):
        """Mulai battle antara dua kartu utama."""
        battle = Battle(self.screen, self.players[0], self.players[1])
        battle.start_battle()

        # Check if 5 rounds are completed
        if self.rounds < 5:
            self.start_battlefield()
        else:
            print("Game Over")

    def start_battlefield(self):
        """Mulai layar battlefield untuk persiapan battle."""
        running = True
        while running:
            self.draw_battlefield()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Klik kiri
                        self.handle_click(event.pos)

                # Escape untuk keluar
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.clock.tick(30)

        self.turn_start_time = pygame.time.get_ticks()
        self.current_player_idx = 0
        self.turns_taken = 0


# Contoh penggunaan
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battlefield Example")

    class Player:
        def __init__(self, name):
            self.name = name
            self.cards = []

        def add_card(self, card):
            self.cards.append(card)

    player1 = Player("Player 1")
    player1.add_card(Card("Dragon", 100, 20, 50))
    player1.add_card(Card("Phoenix", 80, 25, 40))
    player1.add_card(Card("Knight", 90, 15, 30))

    player2 = Player("Player 2")
    player2.add_card(Card("Goblin", 60, 10, 20))
    player2.add_card(Card("Orc", 110, 30, 50))
    player2.add_card(Card("Elf", 70, 20, 30))

    battlefield = Battlefield(screen, [player1, player2])
    battlefield.start_battlefield()