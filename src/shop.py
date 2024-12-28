import pygame
from card import Card
class Shop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 30)
        self.cards = [
            Card("Card1", 50, 10, 20),
            Card("Card2", 60, 15, 30),
            Card("Card3", 70, 20, 40),
            Card("Card3", 70, 25,40),
            Card("Card3", 56, 23, 42)
        ]
        self.selected_card = None
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180
        self.purchased_cards = []

    def draw_shop(self):
        self.screen.fill((50, 50, 50))
        start_x = 100
        for i, card in enumerate(self.cards):
            x = start_x + (self.CARD_WIDTH + 20) * i
            y = 100
            is_selected = self.selected_card == card
            self.draw_card(card, (x, y), is_selected=is_selected)

        # Draw buttons
        close_button = pygame.Rect(650, 50, 100, 40)
        pygame.draw.rect(self.screen, (100, 255, 100), close_button)
        close_text = self.font.render("Close", True, (255, 255, 255))
        self.screen.blit(close_text, (close_button.x + 10, close_button.y + 5))

        purchase_button = pygame.Rect(650, 100, 100, 40)
        pygame.draw.rect(self.screen, (100, 255, 100), purchase_button)
        purchase_text = self.font.render("Purchase", True, (255, 255, 255))
        self.screen.blit(purchase_text, (purchase_button.x + 10, purchase_button.y + 5))

        refresh_button = pygame.Rect(650, 150, 100, 40)
        pygame.draw.rect(self.screen, (100, 255, 100), refresh_button)
        refresh_text = self.font.render("Refresh", True, (255, 255, 255))
        self.screen.blit(refresh_text, (refresh_button.x + 10, refresh_button.y + 5))

        pygame.display.flip()

    def draw_card(self, card, pos, is_selected=False):
        card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        border_color = (255, 255, 0) if is_selected else (0, 0, 0)
        border_width = 5 if is_selected else 2
        pygame.draw.rect(self.screen, border_color, card_rect, border_width)
        pygame.draw.rect(self.screen, (100, 100, 250), card_rect)
        name_text = self.font.render(card.name, True, (255, 255, 255))
        self.screen.blit(name_text, (pos[0] + 10, pos[1] + 10))
        hp_text = self.font.render(f"HP: {card.health}", True, (255, 255, 255))
        self.screen.blit(hp_text, (pos[0] + 10, pos[1] + 50))
        atk_text = self.font.render(f"ATK: {card.attack}", True, (255, 255, 255))
        self.screen.blit(atk_text, (pos[0] + 10, pos[1] + 90))
        price_text = self.font.render(f"Price: {card.price}", True, (255, 255, 255))
        self.screen.blit(price_text, (pos[0] + 10, pos[1] + 130))

    def handle_click(self, pos):
        start_x = 100
        for i, card in enumerate(self.cards):
            card_rect = pygame.Rect(start_x + (self.CARD_WIDTH + 20) * i, 100, self.CARD_WIDTH, self.CARD_HEIGHT)
            if card_rect.collidepoint(pos):
                self.selected_card = card
                print(f"Selected card: {card.name}")
                return

        close_button = pygame.Rect(650, 50, 100, 40)
        purchase_button = pygame.Rect(650, 100, 100, 40)
        refresh_button = pygame.Rect(650, 150, 100, 40)
        if close_button.collidepoint(pos):
            self.close_shop()
        if purchase_button.collidepoint(pos):
            self.purchase_card()
        if refresh_button.collidepoint(pos):
            self.refresh_shop()

    def purchase_card(self):
        if self.selected_card and self.player.coins >= self.selected_card.price:
            self.player.cards.append(self.selected_card)
            self.player.coins -= self.selected_card.price
            self.cards.remove(self.selected_card)
            self.selected_card = None
            print("Card purchased!")
        else:
            print("Not enough coins or no card selected.")

    def refresh_shop(self):
        refresh_cost = 10  # Cost to refresh the shop
        if self.player.coins >= refresh_cost:
            self.player.coins -= refresh_cost
            self.cards = [
                Card("Card4", 80, 25, 50),
                Card("Card5", 90, 30, 60),
                Card("Card6", 100, 35, 70)
            ]
            self.selected_card = None
            print("Shop refreshed!")
        else:
            print("Not enough coins to refresh the shop.")

    def close_shop(self):
        self.screen.fill((50, 50, 50))
        pygame.display.flip()
        self.selected_card = None
        print("Shop closed")
