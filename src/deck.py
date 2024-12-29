import pygame
import sys
from card import Card, Warrior, Archer, Guardian, Assassin

class Deck:
    def __init__(self, screen, players):
        self.screen = screen
        self.players = players
        self.deck = [
        
            Warrior("Warrior", 15, 0.3, 90, 1, 6),
            Archer("Archer", 12, 0.2, 70, 1, 6),
            Guardian("Guardian", 15, 0.6, 130, 1, 6),
            Assassin("Assassin", 28, 0.25, 75, 1, 6),

        ]
        self.font = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()

    def show_deck(self):
        BG_COLOR = (20, 20, 20)
        TEXT_COLOR = (255, 255, 255)
        SELECTED_COLOR = (50, 150, 50)

        current_player_idx = 0

        while self.deck:
            self.screen.fill(BG_COLOR)

            # Display available cards
            y_offset = 100
            for idx, card in enumerate(self.deck):
                card_text = f"{card.name} (HP: {card.health}, ATK: {card.attack})"
                text_surface = self.font.render(card_text, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(400, y_offset))

                pygame.draw.rect(
                    self.screen,
                    SELECTED_COLOR if idx == current_player_idx else BG_COLOR,
                    text_rect.inflate(20, 10)
                )
                self.screen.blit(text_surface, text_rect)
                y_offset += 60

            # Display current player
            player_text = f"{self.players[0].name}, pilih kartu:"
            player_surface = self.font.render(player_text, True, TEXT_COLOR)
            self.screen.blit(player_surface, (200, 50))

            pygame.display.flip()

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
                        chosen_card = self.deck.pop(current_player_idx)
                        self.players[0].cards.append(chosen_card)
                        self.players.append(self.players.pop(0))
                        current_player_idx = 0

                        if not self.deck:
                            return  # End selection

            self.clock.tick(30)