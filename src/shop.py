
# import pygame
# import sys
# import random
# from card import Warrior, Archer, Guardian, Assassin



# class Shop(GameObject):
#     def __init__(self, screen, player):
#         self.screen = screen
#         self.player = player
#         self.cards = [
#             Warrior("Warrior", 15, 0.3, 90, 1, 6, "assets/card.png"),
#             Archer("Archer", 12, 0.2, 70, 1, 6, "assets/card.png"),
#             Guardian("Guardian", 15, 0.6, 130, 1, 6, "assets/card.png"),
#             Assassin("Assassin", 28, 0.25, 75, 1, 6, "assets/card.png"),
#         ] 
#         self.random_card = random.sample(self.cards, 3)
#         self.card_positions = [(354, 399), (561, 396), (774, 396)]
        
        
#         self.CARD_WIDTH = 150
#         self.CARD_HEIGHT = 200
#         self.font = pygame.font.Font(None, 40)
#         self.small_font = pygame.font.Font(None, 20)
#         self.button_font = pygame.font.Font(None, 20)  # Smaller font for buttons
#         self.bold_font = pygame.font.Font(None, 25)  # Slightly larger font for player's coins
#         self.bold_font.set_bold(True)
#         self.stats_font = pygame.font.Font(None, 12)  # Font for card statistics
#         self.stats_font.set_bold(True)
#         self.selected_card = None
#         self.BG_IMAGE_PATH = "assets/shop.png"
#         self.bg_image = pygame.image.load(self.BG_IMAGE_PATH)
#         self.bg_image = pygame.transform.scale(self.bg_image, screen.get_size())
#         self.button_buy = pygame.image.load("assets/buy.png")
#         self.button_buy = pygame.transform.scale(self.button_buy, (101, 40))
#         self.button_refresh = pygame.image.load("assets/refresh.png")
#         self.button_refresh = pygame.transform.scale(self.button_refresh, (101, 40))
       
#         # Initialize buttons
#         self.close_button = pygame.Rect(1165, 25, 100, 40)  # Updated coordinates
#         self.purchase_buttons = [
#             pygame.Rect(367, 667, 100, 40),
#             pygame.Rect(585, 667, 100, 40),
#             pygame.Rect(797, 667, 100, 40)
#         ]
#         self.refresh_button = pygame.Rect(589, 336, 100, 40)  # Updated coordinates

#     def draw_shop(self):
#         self.screen.blit(self.bg_image, (0, 0))
        
#         # Create an instance of CardManager
    
        
#         for i, card in enumerate(self.random_card):
#             x, y = self.card_positions[i]
#             is_selected = self.selected_card == card
            
#             # Use the CardManager instance to draw the card
#             self.draw_card(card, (x, y), border=is_selected)

#         # Draw buttons
#         self.screen.blit(self.button_buy, (self.purchase_buttons[0].x, self.purchase_buttons[0].y))
#         self.screen.blit(self.button_buy, (self.purchase_buttons[1].x, self.purchase_buttons[1].y))
#         self.screen.blit(self.button_buy, (self.purchase_buttons[2].x, self.purchase_buttons[2].y))
#         self.screen.blit(self.button_refresh, (self.refresh_button.x, self.refresh_button.y))

#         # Draw close button with new design
#         pygame.draw.rect(self.screen, (219, 91, 93), self.close_button, border_radius=10)  # DB5B5D color with rounded corners
#         close_text = self.button_font.render("Close", True, (0, 0, 0))  # Black font color
#         close_text_rect = close_text.get_rect(center=self.close_button.center)
#         self.screen.blit(close_text, close_text_rect)

#         # Display player's coin count
#         coin_text = self.bold_font.render(f"{self.player.get_coins()}", True, (255, 255, 255))
#         self.screen.blit(coin_text, (1069, 30))

#         # Display card prices
#         for i, card in enumerate(self.random_card):
#             x = [430, 657, 878][i]
#             price_text = self.small_font.render(f"Price: {card.price}", True, (255, 255, 255))
#             self.screen.blit(price_text, (x, 599))

#         # Display refresh cost
#         refresh_cost_text = self.small_font.render("Cost: 10", True, (255, 255, 255))
#         self.screen.blit(refresh_cost_text, (self.refresh_button.x + 110, self.refresh_button.y + 5))

#         pygame.display.flip()


#     # def draw_player_cards(self, player):
#     #     """Draw the cards of the current player."""
#     #     for i, card in enumerate(player.cards):
#     #         pos = (100 + i * (150 + 14), 100)  # Example position
#     #         border = card == player.selected_card  # Assuming player has a selected_card attribute
#     #         self.card_manager.draw_card(card, pos, border) 


#     def handle_click(self, pos):
#         for i, card in enumerate(self.random_card):
#             card_rect = pygame.Rect(self.card_positions[i][0], self.card_positions[i][1], self.CARD_WIDTH, self.CARD_HEIGHT)
#             if card_rect.collidepoint(pos):
#                 self.selected_card = card
#                 print(f"Selected card: {card.name}")
#                 return

#         if self.close_button.collidepoint(pos):
#             self.close_shop()
#         for i, button in enumerate(self.purchase_buttons):
#             if button.collidepoint(pos):
#                 self.purchase_card()
#                 return
#         if self.refresh_button.collidepoint(pos):
#             self.refresh_shop()

#     def purchase_card(self):
#         if self.selected_card and self.player.get_coins() >= self.selected_card.price and len(self.player.cards) <= 5:
#             self.player.cards.append(self.selected_card)
#             self.player.set_coins(self.player.get_coins() - self.selected_card.price)
#             self.random_card.remove(self.selected_card)
#             self.selected_card = None
#             print("Card purchased!")
#         else:
#             print("Not enough coins or no card selected, or too many cards.")

#     def refresh_shop(self):
#         refresh_cost = 10
#         if self.player.get_coins() >= refresh_cost:
#             self.player.set_coins(self.player.get_coins() - refresh_cost)
#             self.random_card = random.sample(self.cards, 3)
#             self.selected_card = None
#             print("Shop refreshed!")
#         else:
#             print("Not enough coins to refresh the shop.")


#     def close_shop(self):
#         self.screen.fill((50, 50, 50))
#         pygame.display.flip()
#         self.selected_card = None
#         print("Shop closed")
