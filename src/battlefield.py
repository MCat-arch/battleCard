import pygame
import sys
import random
# from shop import Shop
from card import Card, Assassin, Guardian, Warrior, Archer
from result import Result

class GameObject:
    """Base class for all game objects to handle common functionalities."""
    def __init__(self, screen):
        self.screen = screen
        self.screen = pygame.display.set_mode((1280, 720))  # Harus menjadi Surface
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.BG_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (255, 255, 255)
        self.CARD_WIDTH = 150
        self.CARD_HEIGHT = 200

    def draw_text(self, text, position, color=(255, 255, 255)):
        """Helper method to draw text on the screen."""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)
        
    def draw_card(self, card, pos, border=False):
        card_rect = pygame.Rect(pos[0], pos[1], 150, 200)
        if border:
            pygame.draw.rect(self.screen, (255, 255, 0), card_rect.inflate(10, 10), 5)
        self.screen.blit(card.image, (pos[0], pos[1]))
        self.display_card_info(card, pos)

    def display_card_info(self, card, pos):   
        self.small_font = pygame.font.Font(None, 20)
        name_text = self.small_font.render(card.name, True, (255,255,255))
        self.screen.blit(name_text, (pos[0] + 50, pos[1] + 17))

        hp_text = self.small_font.render(f"ATK: {card.attack}", True, (255,255,255))
        self.screen.blit(hp_text, (pos[0] + 50, pos[1] + 140))

        atk_text = self.small_font.render(f"HP: {card.health}", True, (255,255,255))
        self.screen.blit(atk_text, (pos[0] + 50, pos[1] + 160))

class Shop(GameObject):
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.cards = [
            Warrior("Warrior", 15, 0.3, 90, 1, 6, "assets/card.png"),
            Archer("Archer", 12, 0.2, 70, 1, 6, "assets/card.png"),
            Guardian("Guardian", 15, 0.6, 130, 1, 6, "assets/card.png"),
            Assassin("Assassin", 28, 0.25, 75, 1, 6, "assets/card.png"),
        ] 
        self.random_card = random.sample(self.cards, 3)
        self.card_positions = [(354, 399), (561, 396), (774, 396)]
        
        
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 20)
        self.button_font = pygame.font.Font(None, 20)  # Smaller font for buttons
        self.bold_font = pygame.font.Font(None, 25)  # Slightly larger font for player's coins
        self.bold_font.set_bold(True)
        self.stats_font = pygame.font.Font(None, 12)  # Font for card statistics
        self.stats_font.set_bold(True)
        self.selected_card = None
        self.BG_IMAGE_PATH = "assets/shop.png"
        self.bg_image = pygame.image.load(self.BG_IMAGE_PATH)
        self.bg_image = pygame.transform.scale(self.bg_image, screen.get_size())
        self.button_buy = pygame.image.load("assets/buy.png")
        self.button_buy = pygame.transform.scale(self.button_buy, (101, 40))
        self.button_refresh = pygame.image.load("assets/refresh.png")
        self.button_refresh = pygame.transform.scale(self.button_refresh, (101, 40))
       
        # Initialize buttons
        self.close_button = pygame.Rect(1165, 25, 100, 40)  # Updated coordinates
        self.purchase_buttons = [
            pygame.Rect(367, 667, 100, 40),
            pygame.Rect(585, 667, 100, 40),
            pygame.Rect(797, 667, 100, 40)
        ]
        self.refresh_button = pygame.Rect(589, 336, 100, 40)  # Updated coordinates

    def draw_shop(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        # Create an instance of CardManager
    
        
        for i, card in enumerate(self.random_card):
            x, y = self.card_positions[i]
            is_selected = self.selected_card == card
            
            # Use the CardManager instance to draw the card
            self.draw_card(card, (x, y), border=is_selected)

        # Draw buttons
        self.screen.blit(self.button_buy, (self.purchase_buttons[0].x, self.purchase_buttons[0].y))
        self.screen.blit(self.button_buy, (self.purchase_buttons[1].x, self.purchase_buttons[1].y))
        self.screen.blit(self.button_buy, (self.purchase_buttons[2].x, self.purchase_buttons[2].y))
        self.screen.blit(self.button_refresh, (self.refresh_button.x, self.refresh_button.y))

        # Draw close button with new design
        pygame.draw.rect(self.screen, (219, 91, 93), self.close_button, border_radius=10)  # DB5B5D color with rounded corners
        close_text = self.button_font.render("Close", True, (0, 0, 0))  # Black font color
        close_text_rect = close_text.get_rect(center=self.close_button.center)
        self.screen.blit(close_text, close_text_rect)

        # Display player's coin count
        coin_text = self.bold_font.render(f"{self.player.get_coins()}", True, (255, 255, 255))
        self.screen.blit(coin_text, (1069, 30))

        # Display card prices
        for i, card in enumerate(self.random_card):
            x = [430, 657, 878][i]
            price_text = self.small_font.render(f"Price: {card.price}", True, (255, 255, 255))
            self.screen.blit(price_text, (x, 599))

        # Display refresh cost
        refresh_cost_text = self.small_font.render("Cost: 10", True, (255, 255, 255))
        self.screen.blit(refresh_cost_text, (self.refresh_button.x + 110, self.refresh_button.y + 5))

        pygame.display.flip()


    def handle_click(self, pos):
        for i, card in enumerate(self.random_card):
            card_rect = pygame.Rect(self.card_positions[i][0], self.card_positions[i][1], self.CARD_WIDTH, self.CARD_HEIGHT)
            if card_rect.collidepoint(pos):
                self.selected_card = card
                print(f"Selected card: {card.name}")
                return

        if self.close_button.collidepoint(pos):
            self.close_shop()
        for i, button in enumerate(self.purchase_buttons):
            if button.collidepoint(pos):
                self.purchase_card()
                return
        if self.refresh_button.collidepoint(pos):
            self.refresh_shop()

    def purchase_card(self):
        if self.selected_card and self.player.get_coins() >= self.selected_card.price and len(self.player.cards) <= 5:
            self.player.cards.append(self.selected_card)
            self.player.set_coins(self.player.get_coins() - self.selected_card.price)
            self.random_card.remove(self.selected_card)
            self.selected_card = None
            print("Card purchased!")
        else:
            print("Not enough coins or no card selected, or too many cards.")

    def refresh_shop(self):
        refresh_cost = 10
        if self.player.get_coins() >= refresh_cost:
            self.player.set_coins(self.player.get_coins() - refresh_cost)
            self.random_card = random.sample(self.cards, 3)
            self.selected_card = None
            print("Shop refreshed!")
        else:
            print("Not enough coins to refresh the shop.")


    def close_shop(self):
        self.screen.fill((50, 50, 50))
        pygame.display.flip()
        self.selected_card = None
        print("Shop closed")


class PreBattle(GameObject):
    def __init__(self, screen, players):
        super().__init__(screen)
        self.players = players
        self.rounds = 0
        self.turns_taken = 0
        self.shop = None
        self.shop_active = False
        self.shop_cards = []
        self.turn_time = 5  # 20 seconds per turn
        self.turn_start_time = pygame.time.get_ticks()
        self._initialize_ui()

    def _initialize_ui(self):
        """Initialize buttons and background."""
        self.bg_image = pygame.image.load("assets/prebattle.png")
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())
        self.button_upgrade = self._load_button("assets/upgrade.png", (162, 85), (164, 275))
        self.button_swap = self._load_button("assets/swap.png", (162, 85), (990, 275))
        self.button_shop = self._load_button("assets/shop_button.png", (120, 120), (120, 535))
        self.button_next = self._load_button("assets/next.png", (120, 120), (1040, 535))

    def _load_button(self, path, size, position):
        """Load and return a button image and rect."""
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        rect = pygame.Rect(*position, *size)
        return image, rect

    def draw_buttons(self):
        """Draw all buttons on the screen."""
        for image, rect in [self.button_upgrade, self.button_swap, self.button_shop, self.button_next]:
            self.screen.blit(image, rect.topleft)
        pygame.display.flip()

    def handle_click(self, pos):
        """Handle button clicks."""
        if self.button_upgrade[1].collidepoint(pos):
            print("Upgrade clicked")
            self.merge_card()
        if self.button_swap[1].collidepoint(pos):
            print("Swap clicked")
            self.swap_card()
        if self.button_shop[1].collidepoint(pos):
            print("Shop clicked")
            self.open_shop()
        if self.button_next[1].collidepoint(pos):
            print("Next clicked")
            self._next_turn()
            return
        if self.shop_active:
            self.shop.handle_click(pos)
            if self.shop.close_button.collidepoint(pos):
                self.close_shop()
        else:
            # Check for clicks on main cards
            current_player = self.players[self.current_player_idx]
            main_card_positions = [(470, 211), (653, 211)]
            for i in range(2):
                card_rect = pygame.Rect(main_card_positions[i][0], main_card_positions[i][1], self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    # Save the main card based on the clicked position
                    if len(current_player.main_card) < 2:  # Ensure we only have two main cards
                        current_player.main_card.append(current_player.cards[i])  # Append the selected card
                    else:
                        current_player.main_card[i] = current_player.cards[i]  # Replace the existing main card
                    self.selected_main_card_index = i
                    print(f"Selected main card at index {i}: {current_player.main_card[i].name}")
                    return

            # Check for clicks on regular cards for merging
            start_x = 283
            y = 495
            gap = 40
            for i in range(2, len(current_player.cards)):
                card_rect = pygame.Rect(start_x + (self.CARD_WIDTH + gap) * (i - 2), y, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    self.selected_regular_card_index = i
                    print(f"Selected regular card at index {i}: {current_player.cards[i].name}")
                    return

            # Check for clicks on regular cards for swapping
            for i in range(2, len(current_player.cards)):
                card_rect = pygame.Rect(start_x + (self.CARD_WIDTH + gap) * (i - 2), y, self.CARD_WIDTH, self.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    if hasattr(self, 'selected_main_card_index'):
                        self.swap_card(i)  # Perform the swap if a main card is selected
                        print(f"Swapped card at index {i} with main card {self.selected_main_card_index}")
                    return

    def _next_turn(self):
        """Advance to the next turn or start the battle."""
        self.turns_taken += 1
        if self.turns_taken >= len(self.players):
            self.turns_taken = 0
            self.start_battle()
            
    def close_shop(self):
        """Tutup shop."""
        self.shop_active = False
        self.shop = None
        print("Shop closed")


    def swap_card(self):
        """Swap kartu utama dengan kartu lain."""
        current_player = self.players[self.current_player_idx]
        if hasattr(self, 'selected_main_card_index') and hasattr(self, 'selected_regular_card_index'):
            current_player.cards[self.selected_main_card_index], current_player.cards[self.selected_regular_card_index] = (
                current_player.cards[self.selected_regular_card_index],
                current_player.cards[self.selected_main_card_index],
            )
            print(f"Swapped card at index {self.selected_regular_card_index} with main card {self.selected_main_card_index}")
            del self.selected_main_card_index
            del self.selected_regular_card_index
        else:
            print("Select a main card and a regular card to swap.")

    def draw_battlefield(self):
        """Gambar battlefield di layar."""
        self.screen.blit(self.bg_image, (0, 0))
        # Tampilkan nama pemain
       
        if self.shop_active:
            self.shop.draw_shop()
        else:
            self.screen.blit(self.bg_image, (0, 0))
            
            # Get the current player
            current_player = self.players[self.current_player_idx]
            cp_name_text = self.font.render(current_player.name, True, (255, 255, 255))
            self.screen.blit(cp_name_text, (330, 41))

            # Draw main cards
            main_card_positions = [(470, 211), (653, 211)]
            for i in range(2):
                if i < len(current_player.cards):
                    main_card = current_player.cards[i]
                    is_selected = hasattr(self, 'selected_card_index') and self.selected_card_index == i
                    self.draw_card(main_card, main_card_positions[i], border=is_selected)

            # Draw additional cards
            start_x = 283
            y = 495
            gap = 40
            for i, card in enumerate(current_player.cards[2:], start=2):
                x = start_x + (self.CARD_WIDTH + gap) * (i - 2)
                is_selected = hasattr(self, 'selected_regular_card_index') and self.selected_regular_card_index == i
                self.draw_card(card, (x, y), border=is_selected)

            # Draw shop cards
            if self.shop_cards:
                for i, card in enumerate(self.shop_cards):
                    x = start_x + (self.CARD_WIDTH + gap) * (len(current_player.cards) - 2 + i)
                    is_selected = hasattr(self, 'selected_regular_card_index') and self.selected_regular_card_index == i
                    self.draw_card(card, (x, y), border=is_selected)

            # Gambar tombol Merge dan Shop
            self.draw_buttons()

            # Gambar timer
            elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000
            remaining_time = max(0, self.turn_time - elapsed_time)
            timer_text = f"Time left: {int(remaining_time)}s"
            timer_surface = self.font.render(timer_text, True, self.TEXT_COLOR)
            self.screen.blit(timer_surface, (587, 41))

            pygame.display.flip()
        


    def merge_card(self):
        current_player = self.players[self.current_player_idx]

        if not (hasattr(self, 'selected_main_card_index') and hasattr(self, 'selected_regular_card_index')):
            print("Select a main card and a regular card to merge.")
            return

        main_card = current_player.cards[self.selected_main_card_index]
        regular_card = current_player.cards[self.selected_regular_card_index]

        if main_card.name == regular_card.name and main_card.level == regular_card.level:
            # Create a merged card based on the type of the main card
            card_class = type(main_card)
            merged_card = card_class(
                name=f"{main_card.name} {regular_card.level+1}",
                attack=main_card.attack + regular_card.attack,
                defense=main_card.defense,
                health=main_card.health + regular_card.health,
                level=main_card.level + 1,
                price=main_card.price + regular_card.price,
                link=main_card.link
            )

            # Update the player's card list
            current_player.cards.append(merged_card)
            current_player.cards.remove(main_card)
            current_player.cards.remove(regular_card)
            print(f"Merged cards into: {merged_card.name}")

            # Clear selected indices
            del self.selected_main_card_index
            del self.selected_regular_card_index
        else:
            print("Cards cannot be merged. They must have the same name and level.")

    def open_shop(self):
        """Buka shop untuk menambahkan kartu ke deck shop."""
        self.shop_active = True
        self.shop = Shop(self.screen, self.players[self.current_player_idx])
        print("shop opened")
    
   

    def start_battlefield(self):
        if self.rounds is None:
            self.rounds = 0  # Set to 0 if it's not initialized
        while self.rounds < 3:
            # Existing logic for battle rounds
            print(f"Round: {self.rounds}")
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
                    

        # Display result screen when rounds reach 3
        winner = f"{self.players[0].name}" if self.players[0].get_score() > self.players[1].get_score() else f"{self.players[1].name}"
        score = f"{self.players[0].get_score()} vs {self.players[1].get_score()}"
        result = Result(self.screen, winner, score)
        result.draw_result()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if result.handle_click(event.pos):
                        running = False
                        return "dashboard"  # Return a flag to indicate transition to the dashboard

            pygame.display.flip()

    def start_battle(self):
        self.rounds += 1
        for player in self.players:
            player.main_card = [player.cards[0], player.cards[1]]
        battle = Battle(self.screen, self.players, self.players[0].main_card, self.players[1].main_card)
        battle.start_battle()


class Battle(PreBattle):
    def __init__(self, screen, players, main_cards1, main_cards2):
        super().__init__(screen, players)
        self.rounds = self.rounds
        self.player1 = players[0]
        self.player2 = players[1]
        self.player1_main_card = main_cards1
        self.player2_main_card = main_cards2
        self.background = pygame.image.load("assets/battlefield.png")
        self.selected_card = None
        self.opponent_card = None
        self.current_player = self.player1
        self.ATTACK_COLOR = (255, 0, 0)


    def animate_attack(self, attacker_pos, defender_pos):
        for _ in range(10):
            pygame.draw.line(self.screen, self.ATTACK_COLOR, attacker_pos, defender_pos, 5)
            pygame.display.flip()
            self.clock.tick(30)
            self.screen.blit(self.background, (0, 0))
            self.draw_battlefield()

    def draw_battlefield(self):
        """Draw the battlefield including players' cards."""
        self.screen.blit(self.background, (0, 0))
        self.draw_text(self.player1.name, (618, 8))
        self.draw_text(self.player2.name, (618, 677))
        self._draw_player_cards(self.player1_main_card, (406, 41), self.selected_card)
        self._draw_player_cards(self.player2_main_card, (406, 467), self.opponent_card)
        pygame.display.flip()
        
        pygame.display.flip()
        
        
    def _draw_player_cards(self, cards, position, highlight_card):
        """Helper method to draw player cards."""
        x, y = position
        for card in cards:
            if card:
                self.draw_card(card, (x, y), border=card == highlight_card)
                x += 164  # Adjust for card width + spacing


    def handle_click(self, pos):
        """Handle mouse clicks for card selection."""
        if self.current_player == self.player1:
            self._select_card(pos, self.player1_main_card, (406, 41))
        else:
            self._select_card(pos, self.player2_main_card, (406, 467))

        if self.selected_card:
            if self.current_player == self.player1:
                self._select_opponent_card(pos, self.player2_main_card, (406, 467))
            else:
                self._select_opponent_card(pos, self.player1_main_card, (406, 41))

    def _select_card(self, pos, cards, start_position):
        """Select a card based on mouse position."""
        x, y = start_position
        for card in cards:
            card_rect = pygame.Rect(x, y, 150, 200)
            if card_rect.collidepoint(pos):
                self.selected_card = card
                print(f"Selected {card.name}")
                return
            x += 164

    def _select_opponent_card(self, pos, opponent_cards, start_position):
        """Select an opponent's card to battle."""
        x, y = start_position
        for card in opponent_cards:
            card_rect = pygame.Rect(x, y, 150, 200)
            if card_rect.collidepoint(pos):
                self.opponent_card = card
                print(f"Opponent selected {card.name}")
                self.battle_cards()
                return
            x += 164

    def battle_cards(self):
        """Handle the battle between selected cards."""
        if self.selected_card and self.opponent_card:
            self.animate_attack((260, 290), (540, 290))
            self.opponent_card.health -= self.selected_card.attack
            if self.opponent_card.health <= 0:
                self._remove_card(self.opponent_card)
            self.selected_card, self.opponent_card = None, None
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def _remove_card(self, card):
        """Remove a defeated card."""
        if self.current_player == self.player1:
            self.player2_main_card.remove(card)
        else:
            self.player1_main_card.remove(card)

    def start_battle(self):
        """Start the battle loop."""
        running = True
        while running:
            self.draw_battlefield()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            self.clock.tick(30)
            if not self.player1_main_card or not self.player2_main_card:
                if self.player1.cards:
                    new_score = self.player1.get_score() + 1
                    self.player1.set_score(new_score)

                if self.player2.cards:
                    new_score = self.player2.get_score() + 1
                    self.player2.set_score(new_score)

                self.display_result_round()
                running = False

    def display_result_round(self):
        self.screen.blit(self.background, (0, 0))
        result_text = f"{self.players[1].name} wins" if not self.players[0].cards else f"{self.players[0].name} wins"
        result_surface = self.font.render(result_text, True, self.TEXT_COLOR)
        self.screen.blit(result_surface, (580, 345))
        pygame.display.flip()
        pygame.time.wait(3000)


