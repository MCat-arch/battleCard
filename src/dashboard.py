import pygame
import sys
import random
from input_name import get_player_names
from battlefield import Battlefield
from deck import Deck
from card import Card

def show_dashboard(screen):
    pygame.init()
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    BG_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    HOVER_COLOR = (50, 50, 150)

    buttons = [
        {"text": "Start Game", "pos": (400, 200)},
        {"text": "Settings", "pos": (400, 300)},
        {"text": "Exit", "pos": (400, 400)},
    ]

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            text_surface = font.render(button["text"], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button["pos"])

            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER_COLOR, text_rect.inflate(20, 10))
            else:
                pygame.draw.rect(screen, BG_COLOR, text_rect.inflate(20, 10))

            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if font.render(button["text"], True, TEXT_COLOR).get_rect(center=button["pos"]).collidepoint(mouse_pos):
                        if button["text"] == "Start Game":
                            player1_name, player2_name = get_player_names(screen)
                            if player1_name and player2_name:
                                player1 = Player(player1_name)
                                player2 = Player(player2_name)
                                
                                # Mock kartu pemain
                                player1.cards.append(Card("Dragon", 100, 20, 50))
                                player2.cards.append(Card("Phoenix", 80, 25, 60))

                                # Pemain melempar dadu untuk menentukan urutan
                                player1_roll = player1.roll_dice()
                                player2_roll = player2.roll_dice()

                                if player1_roll > player2_roll:
                                    first_player = player1
                                    second_player = player2
                                elif player2_roll > player1_roll:
                                    first_player = player2
                                    second_player = player1
                                else:
                                    # Jika dadu seri, roll ulang
                                    continue
                                
                                deck = Deck(screen, [first_player, second_player])
                                deck.show_deck()

                                # Setelah urutan ditentukan, masuk ke battlefield
                                battlefield = Battlefield(screen, [first_player, second_player])
                                battlefield.start_battle()

                        elif button["text"] == "Settings":
                            pass  # Tambahkan logika untuk Settings jika perlu
                        elif button["text"] == "Exit":
                            pygame.quit()
                            sys.exit()

        clock.tick(30)

class Card:
    def __init__(self, name, hp, atk, price):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.price = price

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def roll_dice(self):
        return random.randint(1, 6)