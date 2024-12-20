# shop.py
import pygame
from card import Card

class Shop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 40)
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180

        # Kartu di shop dengan harga
        self.shop_cards = [
            Card("Knight", 50, 10, price=50),
            Card("Archer", 30, 15, price=40),
            Card("Mage", 60, 5, price=60)
        ]

    def draw(self):
        """Gambar kartu dan harga di shop."""
        shop_rect = pygame.Rect(500, 100, 300, 400)
        pygame.draw.rect(self.screen, (70, 70, 70), shop_rect)

        for i, card in enumerate(self.shop_cards):
            card_rect = pygame.Rect(shop_rect.x + 10, shop_rect.y + 50 + i * 120, self.CARD_WIDTH, self.CARD_HEIGHT)
            pygame.draw.rect(self.screen, (100, 100, 250), card_rect)

            name_text = self.font.render(f"{card.name} (${card.price})", True, (255, 255, 255))
            self.screen.blit(name_text, (card_rect.x + 10, card_rect.y + 10))

    def handle_click(self, pos):
        """Tangani klik untuk membeli kartu."""
        for i, card in enumerate(self.shop_cards):
            card_rect = pygame.Rect(510, 150 + i * 120, self.CARD_WIDTH, self.CARD_HEIGHT)
            if card_rect.collidepoint(pos):
                self.player.add_card(card)
                self.shop_cards.pop(i)
                break
