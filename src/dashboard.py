import pygame
import sys
import random
from input_name import get_player_names
from battlefield import Battlefield
from deck import Deck
from card import Card, Warrior, Archer, Assassin, Guardian

list_card = [
            Warrior("Warrior", 15, 0.3, 90, 1, 6),
            Archer("Archer", 12, 0.2, 70, 1, 6),
            Guardian("Guardian", 15, 0.6, 130, 1, 6),
            Assassin("Assassin", 28, 0.25, 75, 1, 6),
]

class Dashboard:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()

        self.BG_COLOR = (30, 30, 30)
        self.TEXT_COLOR = (255, 255, 255)
        self.HOVER_COLOR = (50, 50, 150)
        
        self.buttons = [
            {"text": "Start Game", "pos": (400, 200)},
            {"text": "Settings", "pos": (400, 300)},
            {"text": "Exit", "pos": (400, 400)},
        ]

    def show_dashboard(self):
        while True:
            self.screen.fill(self.BG_COLOR)
            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons:
                self.render_button(button, mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(mouse_pos)

            self.clock.tick(30)

    def render_button(self, button, mouse_pos):
        text_surface = self.font.render(button["text"], True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button["pos"])

        if text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.HOVER_COLOR, text_rect.inflate(20, 10))
        else:
            pygame.draw.rect(self.screen, self.BG_COLOR, text_rect.inflate(20, 10))

        self.screen.blit(text_surface, text_rect)

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            text_rect = self.font.render(button["text"], True, self.TEXT_COLOR).get_rect(center=button["pos"])
            if text_rect.collidepoint(mouse_pos):
                if button["text"] == "Start Game":
                    self.start_game()
                elif button["text"] == "Settings":
                    print("Settings clicked (Not Implemented)")
                elif button["text"] == "Exit":
                    pygame.quit()
                    sys.exit()

    def start_game(self):
        player1_name, player2_name = get_player_names(self.screen)
        if player1_name and player2_name:
            player1 = Player(player1_name)
            player2 = Player(player2_name)
            
            # Mock kartu awal
            
            player1.cards.append(random.choice(list_card))
            player2.cards.append(random.choice(list_card))

            # Flip koin menentukan siapa duluan
            coin_flip = random.choice(["player1", "player2"])
            if coin_flip == "player1":
                                    print("Player1 duluan")
                                    first_player = player1
                                    second_player = player2
            else:  # tails
                                    print("Player2 duluan")
                                    first_player = player2
                                    second_player = player1

            # Tampilkan deck pemain (opsional)
            deck = Deck(self.screen, [first_player, second_player])
            deck.show_deck()
            # Mulai pertempuran di Battlefield
            battlefield = Battlefield(self.screen, [first_player, second_player])
            battlefield.start_battlefield()

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.coins = 100



# import pygame
# import sys
# import random
# from input_name import get_player_names
# from battlefield import Battlefield
# from deck import Deck
# from card import Card
# from battle import Battle

# def show_dashboard(screen):
#     pygame.init()
#     font = pygame.font.Font(None, 40)
#     clock = pygame.time.Clock()

#     BG_COLOR = (30, 30, 30)
#     TEXT_COLOR = (255, 255, 255)
#     HOVER_COLOR = (50, 50, 150)

#     buttons = [
#         {"text": "Start Game", "pos": (400, 200)},
#         {"text": "Settings", "pos": (400, 300)},
#         {"text": "Exit", "pos": (400, 400)},
#     ]

#     while True:
#         screen.fill(BG_COLOR)
#         mouse_pos = pygame.mouse.get_pos()

#         for button in buttons:
#             text_surface = font.render(button["text"], True, TEXT_COLOR)
#             text_rect = text_surface.get_rect(center=button["pos"])

#             if text_rect.collidepoint(mouse_pos):
#                 pygame.draw.rect(screen, HOVER_COLOR, text_rect.inflate(20, 10))
#             else:
#                 pygame.draw.rect(screen, BG_COLOR, text_rect.inflate(20, 10))

#             screen.blit(text_surface, text_rect)

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 for button in buttons:
#                     if font.render(button["text"], True, TEXT_COLOR).get_rect(center=button["pos"]).collidepoint(mouse_pos):
#                         if button["text"] == "Start Game":
#                             player1_name, player2_name = get_player_names(screen)
#                             if player1_name and player2_name:
#                                 player1 = Player(player1_name)
#                                 player2 = Player(player2_name)
                                
#                                 # Mock kartu pemain
#                                 player1.cards.append(Card("Dragon", 100, 20, 50))
#                                 player2.cards.append(Card("Phoenix", 80, 25, 60))

#                                 coin_flip = random.choice(["player1", "player2"])
#                                 if coin_flip == "player1":
#                                     print("Player1 duluan")
#                                     first_player = player1
#                                     second_player = player2
#                                 else:  # tails
#                                     print("Player2 duluan")
#                                     first_player = player2
#                                     second_player = player1
                                
#                                 deck = Deck(screen, [first_player, second_player])
#                                 deck.show_deck()

#                                 # Setelah urutan ditentukan, ke battlefield
#                                 battlefield = Battlefield(screen, [first_player, second_player])
#                                 battle = Battle(screen, first_player, second_player)
#                                 battlefield.start_battlefield()

#                         elif button["text"] == "Settings":
#                             pass  # Tambahkan logika untuk Settings jika perlu
#                         elif button["text"] == "Exit":
#                             pygame.quit()
#                             sys.exit()

#         clock.tick(30)

# class Player:
#     def __init__(self, name):
#         self.name = name
#         self.cards = []
