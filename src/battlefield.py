import pygame
import sys
from shop import Shop
from card import Card
# from battle import Battle
class Battlefield:
    pass
class Battle(Battlefield):
    pass
class Battlefield:
    def __init__(self, screen, players):
        self.screen = screen
        self.players = players
        self.player1 = players[0]
        self.player2 = players[1]
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

        # Variables for card selection and merging
        self.selected_main_card_index = None
        self.selected_regular_card_index = None
        self.double_click = False


    def draw_buttons(self):
        """Gambar tombol Swap, Merge, dan Shop."""
        # Tombol Swap
        swap_button = pygame.Rect(50, 450, 100, 40)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, swap_button)
        swap_text = self.font.render("Swap", True, self.TEXT_COLOR)
        self.screen.blit(swap_text, (swap_button.x + 10, swap_button.y + 5))

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


    def open_shop(self):
        """Buka shop untuk menambahkan kartu ke deck shop."""
        self.shop_active = True
        self.shop = Shop(self.screen, self.players[self.current_player_idx])
        print("Shop opened")

    def close_shop(self):
        """Tutup shop."""
        self.shop_active = False
        self.shop = None
        print("Shop closed")

    def handle_click(self, pos):
        """Tangani klik mouse."""
        swap_button = pygame.Rect(50, 450, 100, 40)
        merge_button = pygame.Rect(50, 500, 100, 40)
        shop_button = pygame.Rect(650, 500, 100, 40)

        if swap_button.collidepoint(pos):
            print("Swap clicked")
            self.swap_card()

        if merge_button.collidepoint(pos):
            print("Merge clicked")
            self.merge_card()

        if shop_button.collidepoint(pos):
            print("Shop clicked")
            self.open_shop()

        if self.shop_active:
            self.shop.handle_click(pos)
            close_button = pygame.Rect(650, 50, 100, 40)
            purchase_button = pygame.Rect(650, 100, 100, 40)
            if close_button.collidepoint(pos):
                self.close_shop()
            if purchase_button.collidepoint(pos):
                self.shop.purchase_card()
        else:
            # Cek klik pada kartu utama untuk swap atau merge
            current_player = self.players[self.current_player_idx]
            for i in range(2):
                card_rect = pygame.Rect(340 + i * (self.CARD_WIDTH + 20), 100, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    if hasattr(self, 'selected_main_card_index') and self.selected_main_card_index == i:
                        if hasattr(self, 'double_click_main'):
                            del self.double_click_main
                            self.selected_main_card_index = i
                            print(f"Selected main card for merging at index {i}")
                        else:
                            self.double_click_main = True
                            print(f"Double-click detected on main card at index {i}")
                    else:
                        self.selected_main_card_index = i
                        print(f"Selected main card at index {i}")
                    return

            # Cek klik pada kartu biasa untuk merge
            for i in range(2, len(current_player.cards)):
                card_rect = pygame.Rect(200 + (self.CARD_WIDTH + 20) * (i - 2), 300, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    if hasattr(self, 'selected_regular_card_index') and self.selected_regular_card_index == i:
                        if hasattr(self, 'double_click_regular'):
                            del self.double_click_regular
                            self.selected_regular_card_index = i
                            print(f"Selected regular card for merging at index {i}")
                        else:
                            self.double_click_regular = True
                            print(f"Double-click detected on regular card at index {i}")
                    else:
                        self.selected_regular_card_index = i
                        print(f"Selected regular card at index {i}")
                    return

            # Cek klik pada kartu biasa untuk swap
            for i in range(2, len(current_player.cards)):
                card_rect = pygame.Rect(200 + (self.CARD_WIDTH + 20) * (i - 2), 300, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    self.swap_card(i)
                    print(f"Swapped card at index {i} with main card {self.selected_main_card_index}")
                    return


    def draw_battlefield(self):
        """Gambar battlefield di layar."""
        self.screen.fill(self.BG_COLOR)

        if self.shop_active:
            self.shop.draw_shop()
        else:
            # Gambar kartu utama
            current_player = self.players[self.current_player_idx]
            for i in range(2):
                if i < len(current_player.cards):
                    main_card = current_player.cards[i]
                    is_selected = hasattr(self, 'selected_main_card_index') and self.selected_main_card_index == i
                    is_double_clicked = hasattr(self, 'double_click_main') and self.selected_main_card_index == i
                    self.draw_card(main_card, (340 + i * (self.CARD_WIDTH + 20), 100), is_selected=is_selected, is_double_clicked=is_double_clicked)

            # Gambar kartu tambahan
            if len(current_player.cards) > 2:
                start_x = 200
                gap = 20
                for i, card in enumerate(current_player.cards[2:], start=2):
                    x = start_x + (self.CARD_WIDTH + gap) * (i - 2)
                    y = 300
                    is_selected = hasattr(self, 'selected_regular_card_index') and self.selected_regular_card_index == i
                    is_double_clicked = hasattr(self, 'double_click_regular') and self.selected_regular_card_index == i
                    self.draw_card(card, (x, y), is_selected=is_selected, is_double_clicked=is_double_clicked)

            # Gambar deck kartu hasil shop
            if self.shop_cards:
                start_x = 340
                for i, card in enumerate(self.shop_cards):
                    x = start_x + (self.CARD_WIDTH + 10) * i
                    y = 500
                    self.draw_card(card, (x, y), self.DECK_COLOR)

            # Gambar tombol Swap, Merge, dan Shop
            self.draw_buttons()

            # Gambar timer
            elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000
            remaining_time = max(0, self.turn_time - elapsed_time)
            timer_text = f"Time left: {int(remaining_time)}s"
            timer_surface = self.font.render(timer_text, True, self.TEXT_COLOR)
            self.screen.blit(timer_surface, (340, 50))

        pygame.display.flip()



    def draw_card(self, card, pos, color=None, is_selected=False, is_double_clicked=False):
        """Gambar kartu di layar dengan efek klik."""
        # Perbesar kartu jika diklik (dipilih)
        scale_factor = 1.1 if is_selected else 1
        scaled_width = int(self.CARD_WIDTH * scale_factor)
        scaled_height = int(self.CARD_HEIGHT * scale_factor)
        scaled_pos = (pos[0] - (scaled_width - self.CARD_WIDTH) // 2, pos[1] - (scaled_height - self.CARD_HEIGHT) // 2)
        
        card_rect = pygame.Rect(scaled_pos[0], scaled_pos[1], scaled_width, scaled_height)
        border_color = (255, 255, 0) if is_double_clicked else (0, 0, 0)
        border_width = 5 if is_double_clicked else 2
        
        # Gambar border kartu
        pygame.draw.rect(self.screen, border_color, card_rect, border_width)
        pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)
        
        # Tampilkan informasi kartu
        name_text = self.font.render(card.name, True, self.TEXT_COLOR)
        self.screen.blit(name_text, (scaled_pos[0] + 10, scaled_pos[1] + 10))

        hp_text = self.font.render(f"HP: {card.health}", True, self.TEXT_COLOR)
        self.screen.blit(hp_text, (scaled_pos[0] + 10, scaled_pos[1] + 50))

        atk_text = self.font.render(f"ATK: {card.attack}", True, self.TEXT_COLOR)
        self.screen.blit(atk_text, (scaled_pos[0] + 10, scaled_pos[1] + 90))



                
    def swap_card(self, index):
        """Swap kartu utama dengan kartu lain."""
        current_player = self.players[self.current_player_idx]
        if hasattr(self, 'selected_main_card_index') and index < len(current_player.cards):
            current_player.cards[self.selected_main_card_index], current_player.cards[index] = (
                current_player.cards[index],
                current_player.cards[self.selected_main_card_index],
            )
            print(f"Swapped card at index {index} with main card {self.selected_main_card_index}")
            del self.selected_main_card_index


        
    def merge_card(self):
        """Merge kartu utama dengan kartu biasa."""
        current_player = self.players[self.current_player_idx]
        if hasattr(self, 'selected_main_card_index') and hasattr(self, 'selected_regular_card_index'):
            main_card = current_player.cards[self.selected_main_card_index]
            regular_card = current_player.cards[self.selected_regular_card_index]
            if main_card.name == regular_card.name and main_card.level == regular_card.level:
                merged_card = Card(
                    name=f"{main_card.name}+{regular_card.name}",
                    health=main_card.health + regular_card.health,
                    attack=main_card.attack + regular_card.attack,
                    level=main_card.level + 1,
                    price=main_card.price
                )
                current_player.cards.append(merged_card)
                current_player.cards.remove(main_card)
                current_player.cards.remove(regular_card)
                print(f"Merged cards into: {merged_card.name}")
                del self.selected_main_card_index
                del self.selected_regular_card_index
            else:
                print("Cards cannot be merged. They must have the same name and level.")
        else:
            print("Select a main card and a regular card to merge.")



    def start_battlefield(self):
        while self.rounds < 3:
            for player in self.players:
                self.current_player_idx = self.players.index(player)
                self.turn_start_time = pygame.time.get_ticks()
                while True:
                    self.draw_battlefield()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.handle_click(event.pos)
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                return
                    elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000
                    if elapsed_time >= self.turn_time:
                        break
                    pygame.display.flip()
                    self.clock.tick(60)

                self.turns_taken += 1
                if self.turns_taken >= len(self.players):
                    self.turns_taken = 0
                    self.start_battle()

    def start_battle(self):
        self.rounds += 1
        # Ensure main cards are set if not manually selected
        if not hasattr(self, 'selected_main_cards') or len(self.selected_main_cards) < 2:
            self.selected_main_cards = [0, 1]  # Default to the first two cards
        selected_cards_player1 = [self.player1.cards[i] for i in self.selected_main_cards]
        selected_cards_player2 = [self.player2.cards[i] for i in self.selected_main_cards]
        battle = Battle(self.screen, [self.player1, self.player2], self.rounds, selected_cards_player1, selected_cards_player2)
        battle.start_battle()

# class Battlefield:
#     def __init__(self, screen, players):
#         self.screen = screen
#         self.players = players
#         self.player1 = players[0]
#         self.player2 = players[1]
#         self.current_player_idx = 0
#         self.turns_taken = 0
#         self.rounds = 0
#         self.font = pygame.font.Font(None, 30)
#         self.clock = pygame.time.Clock()

#         # Warna
#         self.BG_COLOR = (50, 50, 50)
#         self.TEXT_COLOR = (255, 255, 255)
#         self.CARD_COLOR = (100, 100, 250)
#         self.DECK_COLOR = (250, 100, 100)
#         self.BUTTON_COLOR = (100, 255, 100)

#         # Ukuran kartu
#         self.CARD_WIDTH = 120
#         self.CARD_HEIGHT = 180

#         # Menyiapkan Shop
#         self.shop = None
#         self.shop_active = False
#         self.shop_cards = []

#         # Timer
#         self.turn_time = 20  # 20 seconds per turn
#         self.turn_start_time = pygame.time.get_ticks()

#     def draw_card(self, card, pos, color=None, is_selected=False):
#         """Gambar kartu di layar dengan efek klik."""
#         # Perbesar kartu jika diklik (dipilih)
#         scale_factor = 1.1 if is_selected else 1
#         scaled_width = int(self.CARD_WIDTH * scale_factor)
#         scaled_height = int(self.CARD_HEIGHT * scale_factor)
#         scaled_pos = (pos[0] - (scaled_width - self.CARD_WIDTH) // 2, pos[1] - (scaled_height - self.CARD_HEIGHT) // 2)
        
#         card_rect = pygame.Rect(scaled_pos[0], scaled_pos[1], scaled_width, scaled_height)
#         border_color = (255, 255, 0) if is_selected else (0, 0, 0)
#         border_width = 5 if is_selected else 2
        
#         # Gambar border kartu
#         pygame.draw.rect(self.screen, border_color, card_rect, border_width)
#         pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)
        
#         # Tampilkan informasi kartu
#         name_text = self.font.render(card.name, True, self.TEXT_COLOR)
#         self.screen.blit(name_text, (scaled_pos[0] + 10, scaled_pos[1] + 10))

#         hp_text = self.font.render(f"HP: {card.health}", True, self.TEXT_COLOR)
#         self.screen.blit(hp_text, (scaled_pos[0] + 10, scaled_pos[1] + 50))

#         atk_text = self.font.render(f"ATK: {card.attack}", True, self.TEXT_COLOR)
#         self.screen.blit(atk_text, (scaled_pos[0] + 10, scaled_pos[1] + 90))



#     def draw_buttons(self):
#         """Gambar tombol Merge dan Shop."""
#         # Tombol Merge
#         merge_button = pygame.Rect(50, 500, 100, 40)
#         pygame.draw.rect(self.screen, self.BUTTON_COLOR, merge_button)
#         merge_text = self.font.render("Merge", True, self.TEXT_COLOR)
#         self.screen.blit(merge_text, (merge_button.x + 10, merge_button.y + 5))

#         # Tombol Shop
#         shop_button = pygame.Rect(650, 500, 100, 40)
#         pygame.draw.rect(self.screen, self.BUTTON_COLOR, shop_button)
#         shop_text = self.font.render("Shop", True, self.TEXT_COLOR)
#         self.screen.blit(shop_text, (shop_button.x + 15, shop_button.y + 5))

#     def handle_click(self, pos):
#         """Tangani klik mouse."""
#         merge_button = pygame.Rect(50, 500, 100, 40)
#         shop_button = pygame.Rect(650, 500, 100, 40)

#         if merge_button.collidepoint(pos):
#             print("Merge clicked")
#             self.merge_card()

#         if shop_button.collidepoint(pos):
#             print("Shop clicked")
#             self.open_shop()

#         # Cek klik pada kartu utama untuk swap
#         current_player = self.players[self.current_player_idx]
#         for i in range(2):
#             card_rect = pygame.Rect(340 + i * (self.CARD_WIDTH + 20), 100, self.CARD_WIDTH, self.CARD_HEIGHT)
#             if card_rect.collidepoint(pos):
#                 self.selected_card_index = i
#                 print(f"Selected main card at index {i}")
#                 return

#         # Cek klik pada kartu biasa untuk swap
#         for i in range(2, len(current_player.cards)):
#             card_rect = pygame.Rect(200 + (self.CARD_WIDTH + 20) * (i - 2), 300, self.CARD_WIDTH, self.CARD_HEIGHT)
#             if card_rect.collidepoint(pos):
#                 self.swap_card(i)
#                 print(f"Selected regular card at index {i}")
#                 return
            
#     def swap_card(self, index):
#         """Swap kartu utama dengan kartu lain."""
#         current_player = self.players[self.current_player_idx]
#         if index < len(current_player.cards) and hasattr(self, 'selected_card_index'):
#             current_player.cards[self.selected_card_index], current_player.cards[index] = (
#                 current_player.cards[index],
#                 current_player.cards[self.selected_card_index],
#             )
#             print(f"Swapped card at index {index} with main card {self.selected_card_index}")
#             del self.selected_card_index


#     def draw_battlefield(self):
#         """Gambar battlefield di layar."""
#         self.screen.fill(self.BG_COLOR)

#         # Gambar kartu utama
#         current_player = self.players[self.current_player_idx]
#         for i in range(2):
#             if i < len(current_player.cards):
#                 main_card = current_player.cards[i]
#                 is_selected = hasattr(self, 'selected_card_index') and self.selected_card_index == i
#                 self.draw_card(main_card, (340 + i * (self.CARD_WIDTH + 20), 100), is_selected=is_selected)

#         # Gambar kartu tambahan
#         if len(current_player.cards) > 2:
#             start_x = 200
#             gap = 20
#             for i, card in enumerate(current_player.cards[2:], start=2):
#                 x = start_x + (self.CARD_WIDTH + gap) * (i - 2)
#                 y = 300
#                 self.draw_card(card, (x, y))

#         # Gambar deck kartu hasil shop
#         if self.shop_cards:
#             start_x = 340
#             for i, card in enumerate(self.shop_cards):
#                 x = start_x + (self.CARD_WIDTH + 10) * i
#                 y = 500
#                 self.draw_card(card, (x, y), self.DECK_COLOR)

#         # Gambar tombol Merge dan Shop
#         self.draw_buttons()

#         # Gambar timer
#         elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000
#         remaining_time = max(0, self.turn_time - elapsed_time)
#         timer_text = f"Time left: {int(remaining_time)}s"
#         timer_surface = self.font.render(timer_text, True, self.TEXT_COLOR)
#         self.screen.blit(timer_surface, (340, 50))

#         pygame.display.flip()


#     def merge_card(self):
#         """Merge kartu utama dengan kartu dari deck shop."""
#         current_player = self.players[self.current_player_idx]
#         if self.shop_cards:
#             main_card = current_player.cards[0]
#             shop_card = self.shop_cards.pop(0)  # Ambil kartu pertama di shop

#             # Gabungkan atribut kartu
#             merged_card = Card(
#                 name=f"{main_card.name}+{shop_card.name}",
#                 health=main_card.health + shop_card.health,
#                 attack=main_card.attack + shop_card.attack,
#                 price=main_card.price
#             )
#             current_player.cards[0] = merged_card
#             print(f"Merged cards into: {merged_card.name}")


#     def open_shop(self):
#         """Buka shop untuk menambahkan kartu ke deck shop."""
#         self.shop_active = True
#         self.shop = Shop(self.screen, self.players[self.current_player_idx])
#         new_card = Card("ShopCard", 50, 10, 20)  # Contoh kartu shop
#         self.shop_cards.append(new_card)
#         print("Added new card from shop")

#     def start_battlefield(self):
#         while self.rounds < 3:
#             for player in self.players:
#                 self.current_player_idx = self.players.index(player)
#                 self.turn_start_time = pygame.time.get_ticks()
#                 while True:
#                     self.draw_battlefield()
#                     for event in pygame.event.get():
#                         if event.type == pygame.QUIT:
#                             pygame.quit()
#                             sys.exit()
#                         if event.type == pygame.MOUSEBUTTONDOWN:
#                             self.handle_click(event.pos)
#                         elif event.type == pygame.KEYDOWN:
#                             if event.key == pygame.K_ESCAPE:
#                                 return
#                     elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000
#                     if elapsed_time >= self.turn_time:
#                         break
#                     pygame.display.flip()
#                     self.clock.tick(60)

#                 self.turns_taken += 1
#                 if self.turns_taken >= len(self.players):
#                     self.turns_taken = 0
#                     self.start_battle()

#     def start_battle(self):
#         self.rounds += 1
#         # Ensure main cards are set if not manually selected
#         if not hasattr(self, 'selected_main_cards') or len(self.selected_main_cards) < 2:
#             self.selected_main_cards = [0, 1]  # Default to the first two cards
#         selected_cards_player1 = [self.player1.cards[i] for i in self.selected_main_cards]
#         selected_cards_player2 = [self.player2.cards[i] for i in self.selected_main_cards]
#         battle = Battle(self.screen, [self.player1, self.player2], self.rounds, selected_cards_player1, selected_cards_player2)
#         battle.start_battle()



class Battle:
    def __init__(self, screen, players, rounds, selected_cards_player1, selected_cards_player2):
        self.screen = screen
        self.players = players
        self.rounds = rounds
        self.player1 = players[0]
        self.player2 = players[1]
        self.selected_cards_player1 = selected_cards_player1
        self.selected_cards_player2 = selected_cards_player2
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("assets/battlefield.png")
        self.TEXT_COLOR = (255, 255, 255)
        self.CARD_COLOR = (100, 100, 250)
        self.ATTACK_COLOR = (255, 0, 0)
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180
        self.selected_card = None
        self.opponent_card = None
        self.current_player = self.player1
        self.player1_score = 0
        self.player2_score = 0

    def draw_card(self, card, pos, color=None, is_selected=False):
        """Gambar kartu di layar dengan efek klik."""
        # Perbesar kartu jika diklik (dipilih)
        scale_factor = 1.1 if is_selected else 1
        scaled_width = int(self.CARD_WIDTH * scale_factor)
        scaled_height = int(self.CARD_HEIGHT * scale_factor)
        scaled_pos = (pos[0] - (scaled_width - self.CARD_WIDTH) // 2, pos[1] - (scaled_height - self.CARD_HEIGHT) // 2)
        
        card_rect = pygame.Rect(scaled_pos[0], scaled_pos[1], scaled_width, scaled_height)
        border_color = (255, 255, 0) if is_selected else (0, 0, 0)
        border_width = 5 if is_selected else 2
        
        # Gambar border kartu
        pygame.draw.rect(self.screen, border_color, card_rect, border_width)
        pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)
        
        # Tampilkan informasi kartu
        name_text = self.font.render(card.name, True, self.TEXT_COLOR)
        self.screen.blit(name_text, (scaled_pos[0] + 10, scaled_pos[1] + 10))

        hp_text = self.font.render(f"HP: {card.health}", True, self.TEXT_COLOR)
        self.screen.blit(hp_text, (scaled_pos[0] + 10, scaled_pos[1] + 50))

        atk_text = self.font.render(f"ATK: {card.attack}", True, self.TEXT_COLOR)
        self.screen.blit(atk_text, (scaled_pos[0] + 10, scaled_pos[1] + 90))

    def animate_attack(self, attacker_pos, defender_pos):
        for _ in range(10):
            pygame.draw.line(self.screen, self.ATTACK_COLOR, attacker_pos, defender_pos, 5)
            pygame.display.flip()
            self.clock.tick(30)
            self.screen.blit(self.background, (0, 0))
            self.draw_battlefield()

    def draw_battlefield(self):
        self.screen.blit(self.background, (0, 0))
        if self.selected_cards_player1:
            for i, card in enumerate(self.selected_cards_player1):
                border = card == self.selected_card
                self.draw_card(card, (100 + i * (self.CARD_WIDTH + 10), 200), is_selected=border)
        if self.selected_cards_player2:
            for i, card in enumerate(self.selected_cards_player2):
                border = card == self.opponent_card
                self.draw_card(card, (500 + i * (self.CARD_WIDTH + 10), 200), is_selected=border)
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
        if self.selected_card and self.opponent_card:
            self.animate_attack((260, 290), (540, 290))
            self.opponent_card.health -= self.selected_card.attack
            if self.opponent_card.health <= 0:
                if self.current_player == self.player1:
                    self.selected_cards_player2.remove(self.opponent_card)
                else:
                    self.selected_cards_player1.remove(self.opponent_card)
            self.selected_card, self.opponent_card = None, None
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def start_battle(self):
        running = True
        while running:
            self.draw_battlefield()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                    if self.selected_card and self.opponent_card:
                        self.battle_cards()
            self.clock.tick(30)
            if not self.selected_cards_player1 or not self.selected_cards_player2:
                if self.selected_cards_player1:
                    self.player1_score += 1
                if self.selected_cards_player2:
                    self.player2_score += 1
                self.display_result_round()
                running = False

    def display_result_round(self):
        self.screen.blit(self.background, (0, 0))
        result_text = "Player 2 wins!" if not self.selected_cards_player1 else "Player 1 wins!"
        result_surface = self.font.render(result_text, True, self.TEXT_COLOR)
        self.screen.blit(result_surface, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)


# class Battle:
#     def __init__(self, screen, players, rounds, selected_cards_player1, selected_cards_player2):
#         self.screen = screen
#         self.players = players
#         self.rounds = rounds
#         self.player1 = players[0]
#         self.player2 = players[1]
#         self.selected_cards_player1 = selected_cards_player1
#         self.selected_cards_player2 = selected_cards_player2
#         self.font = pygame.font.Font(None, 30)
#         self.clock = pygame.time.Clock()
#         self.background = pygame.image.load("assets/battlefield.png")
#         self.TEXT_COLOR = (255, 255, 255)
#         self.CARD_COLOR = (100, 100, 250)
#         self.ATTACK_COLOR = (255, 0, 0)
#         self.CARD_WIDTH = 120
#         self.CARD_HEIGHT = 180
#         self.selected_card = None
#         self.opponent_card = None
#         self.current_player = self.player1
#         self.player1_score = 0
#         self.player2_score = 0

#     def draw_card(self, card, pos, color=None, border=False):
#         card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
#         if border:
#             pygame.draw.rect(self.screen, (255, 255, 0), card_rect.inflate(10, 10), 5)
#         pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)
#         name_text = self.font.render(card.name, True, self.TEXT_COLOR)
#         self.screen.blit(name_text, (pos[0] + 10, pos[1] + 10))
#         hp_text = self.font.render(f"HP: {card.health}", True, self.TEXT_COLOR)
#         self.screen.blit(hp_text, (pos[0] + 10, pos[1] + 50))
#         atk_text = self.font.render(f"ATK: {card.attack}", True, self.TEXT_COLOR)
#         self.screen.blit(atk_text, (pos[0] + 10, pos[1] + 90))

#     def animate_attack(self, attacker_pos, defender_pos):
#         for _ in range(10):
#             pygame.draw.line(self.screen, self.ATTACK_COLOR, attacker_pos, defender_pos, 5)
#             pygame.display.flip()
#             self.clock.tick(30)
#             self.screen.blit(self.background, (0, 0))
#             self.draw_battlefield()

#     def draw_battlefield(self):
#         self.screen.blit(self.background, (0, 0))
#         if self.selected_cards_player1:
#             for i, card in enumerate(self.selected_cards_player1):
#                 border = card == self.selected_card
#                 self.draw_card(card, (100 + i * (self.CARD_WIDTH + 10), 200), border=border)
#         if self.selected_cards_player2:
#             for i, card in enumerate(self.selected_cards_player2):
#                 border = card == self.opponent_card
#                 self.draw_card(card, (500 + i * (self.CARD_WIDTH + 10), 200), border=border)
#         pygame.display.flip()

#     def handle_click(self, pos):
#         if self.current_player == self.player1:
#             for i, card in enumerate(self.selected_cards_player1):
#                 card_rect = pygame.Rect(100 + i * (self.CARD_WIDTH + 10), 200, self.CARD_WIDTH, self.CARD_HEIGHT)
#                 if card_rect.collidepoint(pos):
#                     self.selected_card = card
#                     print(f"Player 1 selected card: {card.name}")
#                     return
#         else:
#             for i, card in enumerate(self.selected_cards_player2):
#                 card_rect = pygame.Rect(500 + i * (self.CARD_WIDTH + 10), 200, self.CARD_WIDTH, self.CARD_HEIGHT)
#                 if card_rect.collidepoint(pos):
#                     self.opponent_card = card
#                     print(f"Player 2 selected card: {card.name}")
#                     return

#     def battle_cards(self):
#         if self.selected_card and self.opponent_card:
#             self.animate_attack((260, 290), (540, 290))
#             self.opponent_card.health -= self.selected_card.attack
#             if self.opponent_card.health <= 0:
#                 if self.current_player == self.player1:
#                     self.selected_cards_player2.remove(self.opponent_card)
#                 else:
#                     self.selected_cards_player1.remove(self.opponent_card)
#             self.selected_card, self.opponent_card = None, None
#             self.current_player = self.player2 if self.current_player == self.player1 else self.player1

#     def start_battle(self):
#         running = True
#         while running:
#             self.draw_battlefield()
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     self.handle_click(event.pos)
#                     if self.selected_card and self.opponent_card:
#                         self.battle_cards()
#             self.clock.tick(30)
#             if not self.player1.cards or not self.player2.cards:
#                 if self.player1.cards:
#                     self.player1_score += 1
#                 if self.player2.cards:
#                     self.player2_score += 1
#                 self.display_result_round()
#                 running = False

#     def display_result_round(self):
#         self.screen.blit(self.background, (0, 0))
#         result_text = "Player 2 wins!" if not self.player1.cards else "Player 1 wins!"
#         result_surface = self.font.render(result_text, True, self.TEXT_COLOR)
#         self.screen.blit(result_surface, (300, 300))
#         pygame.display.flip()
#         pygame.time.wait(3000)
