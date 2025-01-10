import pygame
import sys
from card import Warrior, Archer, Guardian, Assassin

class Deck:
    def __init__(self, screen, players):
        self.screen = screen
        self.players = players
        self.deck = [
            Warrior("Warrior", 15, 0.3, 90, 1, 6, "assets/card.png"),
            Archer("Archer", 12, 0.2, 70, 1, 6, "assets/card.png"),
            Guardian("Guardian", 15, 0.6, 130, 1, 6, "assets/card.png"),
            Assassin("Assassin", 28, 0.25, 75, 1, 6, "assets/card.png"),
        ]
        
        self.font = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()
        self.selected_card_index = None
        self.CARD_IMAGE_PATH = "assets/card.png"
        try:
            self.card_image = pygame.image.load(self.CARD_IMAGE_PATH)
            self.card_image = pygame.transform.scale(self.card_image, (150, 200))  # Sesuaikan ukuran gambar dengan kartu
        except pygame.error as e:
            print(f"Error loading card image: {e}")
            sys.exit()
        
    def load_background(self, bg_image_path, bg_color):
        try:
            bg_image = pygame.image.load(bg_image_path)
            return pygame.transform.scale(bg_image, self.screen.get_size())
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            sys.exit()


    def draw_background(self, bg_image):
        self.screen.blit(bg_image, (0, 0))


    def draw_cards(self, start_x, start_y, current_player_idx, mouse_pos):
        card_width, card_height = 150, 200
        selected_color, hover_color, bg_color = (50, 150, 50), (150, 150, 150), (20, 20, 20)

        for idx, card in enumerate(self.deck):
            x = start_x + (card_width + 20) * idx
            y = start_y
            card_rect = pygame.Rect(x, y, card_width, card_height)

            border_color = selected_color if idx == current_player_idx else bg_color
            border_width = 5 if idx == current_player_idx else 2

            if card_rect.collidepoint(mouse_pos):
                border_color = hover_color
                border_width = 5

            self.screen.blit(self.card_image, (x, y))

            font_size = pygame.font.Font(None, 20)
            name_text = font_size.render(card.name, True, (255, 255, 255))
            atk_text = font_size.render(f"ATK: {card.attack}", True, (255, 255, 255))
            hp_text = font_size.render(f"HP: {card.health}", True, (255, 255, 255))

            self.screen.blit(name_text, (x + 50, y + 17))
            self.screen.blit(atk_text, (x + 50, y + card_height - 60))
            self.screen.blit(hp_text, (x + 50, y + card_height - 40))


    def draw_player_prompt(self):
        player_text = f"{self.players[0].name}, pilih kartu:"
        player_surface = self.font.render(player_text, True, (20, 20, 20))
        player_rect = player_surface.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(player_surface, player_rect)


    def handle_events(self, current_player_idx):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_player_idx = (current_player_idx - 1) % len(self.deck)
                elif event.key == pygame.K_DOWN:
                    current_player_idx = (current_player_idx + 1) % len(self.deck)
                elif event.key == pygame.K_RETURN:
                    return self.select_card(current_player_idx)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for idx, card in enumerate(self.deck):
                    card_rect = pygame.Rect(
                        self.calculate_card_position(idx, len(self.deck)), 300, 150, 200
                    )
                    if card_rect.collidepoint(mouse_pos):
                        return self.select_card(idx)
        return current_player_idx


    def select_card(self, idx):
        chosen_card = self.deck.pop(idx)
        self.players[0].cards.append(chosen_card)
        self.players.append(self.players.pop(0))
        return 0


    def calculate_card_position(self, idx, deck_size):
        card_width = 150
        start_x = (self.screen.get_width() - (deck_size * (card_width + 20))) // 2
        return start_x + (card_width + 20) * idx


    def show_deck(self):
        bg_image_path = "assets/mainmenu.png"
        bg_image = self.load_background(bg_image_path, (20, 20, 20))

        current_player_idx = 0

        while self.deck:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_background(bg_image)

            start_x = self.calculate_card_position(0, len(self.deck))
            start_y = 300

            self.draw_cards(start_x, start_y, current_player_idx, mouse_pos)
            self.draw_player_prompt()

            pygame.display.flip()

            current_player_idx = self.handle_events(current_player_idx)
            self.clock.tick(60)
