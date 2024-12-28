import pygame
import sys
from card import Card
from battlefield import Battlefield

class Battle(Battlefield) :
    def __init__(self, screen, players, rounds):
        super().__init__(screen, players, rounds)
        self.screen = screen
        self.player1 = players[0]
        self.player2 = players[1]
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load("assets/battlefield.png")

        # Warna
        self.TEXT_COLOR = (255, 255, 255)
        self.CARD_COLOR = (100, 100, 250)
        self.ATTACK_COLOR = (255, 0, 0)

        # Ukuran kartu
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180

        # State
        self.selected_card = None
        self.opponent_card = None
        self.current_player = players[0]

    def draw_card(self, card, pos, color=None):
        """Gambar kartu di layar."""
        card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)

        # Tampilkan informasi kartu
        name_text = self.font.render(card.name, True, self.TEXT_COLOR)
        self.screen.blit(name_text, (pos[0] + 10, pos[1] + 10))

        hp_text = self.font.render(f"HP: {card.health}", True, self.TEXT_COLOR)
        self.screen.blit(hp_text, (pos[0] + 10, pos[1] + 50))

        atk_text = self.font.render(f"ATK: {card.attack}", True, self.TEXT_COLOR)
        self.screen.blit(atk_text, (pos[0] + 10, pos[1] + 90))

    def animate_attack(self, attacker_pos, defender_pos):
        """Animasi serangan."""
        for _ in range(10):
            pygame.draw.line(self.screen, self.ATTACK_COLOR, attacker_pos, defender_pos, 5)
            pygame.display.flip()
            self.clock.tick(30)
            self.screen.blit(self.background, (0, 0))
            self.draw_battlefield()

    def draw_battlefield(self):
        """Gambar battlefield di layar."""
        self.screen.blit(self.background, (0, 0))

        # Gambar kartu utama player 1
        if any(self.player1.cards):
            for i, card in enumerate(self.player1.cards):
                self.draw_card(card, (100 + i * (self.CARD_WIDTH + 10), 200))

        # Gambar kartu utama player 2
        if any(self.player2.cards):
            for i, card in enumerate(self.player2.cards):
                self.draw_card(card, (500 + i * (self.CARD_WIDTH + 10), 200))

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
        """Lakukan battle antara dua kartu yang dipilih."""
        if self.selected_card and self.opponent_card:
            self.animate_attack((260, 290), (540, 290))
            self.opponent_card.health -= self.selected_card.attack
            if self.opponent_card.health <= 0:
                print(f"{self.opponent_card.name} is defeated!")
                if self.current_player == self.player1:
                    self.player2.cards.remove(self.opponent_card)
                else:
                    self.player1.cards.remove(self.opponent_card)

            self.selected_card, self.opponent_card = None, None
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def start_battle(self):
        """Mulai battle antara dua kartu utama."""
        running = True
        while running:
            self.draw_battlefield()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Check if any player has no cards left
            if not self.player1.cards or not self.player2.cards:
                running = False

            self.clock.tick(30)

            # Cek apakah ronde selesai dan tambahkan poin
            if not self.player1.cards or not self.player2.cards:
                if self.player1.cards:
                    self.player1_score += 1
                if self.player2.cards:
                    self.player2_score += 1

                print(f"Round {self.round} selesai!")
                self.round += 1
                
                battlefield = Battlefield()
                # Reset kartu atau lakukan persiapan ronde baru di sini jika perlu
                if self.round > self.max_rounds:
                    running = False

        # Display the result setelah 3 ronde
        self.display_result()


    def display_result_round(self):
        """Tampilkan hasil battle."""
        self.screen.blit(self.background, (0, 0))
        if not self.player1.cards:
            result_text = "Player 2 wins!"
        elif not self.player2.cards:
            result_text = "Player 1 wins!"
        else:
            result_text = "It's a draw!"
        result_surface = self.font.render(result_text, True, self.TEXT_COLOR)
        self.screen.blit(result_surface, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing
    
    def display_result(self):
        print("Pertarungan selesai!")
        print(f"Skor Akhir: Player 1 - {self.player1_score}, Player 2 - {self.player2_score}")
        if self.player1_score > self.player2_score:
            print("Player 1 menang!")
        elif self.player2_score > self.player1_score:
            print("Player 2 menang!")
        else:
            print("Pertandingan seri!")




class Battle:
    def __init__(self, screen, players, rounds):
        self.screen = screen
        self.players = players
        self.rounds = rounds
        self.player1 = players[0]
        self.player2 = players[1]
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

    def draw_card(self, card, pos, color=None, border=False):
        card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        if border:
            pygame.draw.rect(self.screen, (255, 255, 0), card_rect.inflate(10, 10), 5)
        pygame.draw.rect(self.screen, color or self.CARD_COLOR, card_rect)
        name_text = self.font.render(card.name, True, self.TEXT_COLOR)
        self.screen.blit(name_text, (pos[0] + 10, pos[1] + 10))
        hp_text = self.font.render(f"HP: {card.health}", True, self.TEXT_COLOR)
        self.screen.blit(hp_text, (pos[0] + 10, pos[1] + 50))
        atk_text = self.font.render(f"ATK: {card.attack}", True, self.TEXT_COLOR)
        self.screen.blit(atk_text, (pos[0] + 10, pos[1] + 90))

    def animate_attack(self, attacker_pos, defender_pos):
        for _ in range(10):
            pygame.draw.line(self.screen, self.ATTACK_COLOR, attacker_pos, defender_pos, 5)
            pygame.display.flip()
            self.clock.tick(30)
            self.screen.blit(self.background, (0, 0))
            self.draw_battlefield()

    def draw_battlefield(self):
        self.screen.blit(self.background, (0, 0))
        if self.player1.cards:
            for i, card in enumerate(self.player1.cards):
                border = card == self.selected_card
                self.draw_card(card, (100 + i * (self.CARD_WIDTH + 10), 200), border=border)
        if self.player2.cards:
            for i, card in enumerate(self.player2.cards):
                border = card == self.opponent_card
                self.draw_card(card, (500 + i * (self.CARD_WIDTH + 10), 200), border=border)
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
                    self.player2.cards.remove(self.opponent_card)
                else:
                    self.player1.cards.remove(self.opponent_card)
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
            if not self.player1.cards or not self.player2.cards:
                if self.player1.cards:
                    self.player1_score += 1
                if self.player2.cards:
                    self.player2_score += 1
                self.display_result_round()
                running = False

    def display_result_round(self):
        self.screen.blit(self.background, (0, 0))
        result_text = "Player 2 wins!" if not self.player1.cards else "Player 1 wins!"
        result_surface = self.font.render(result_text, True, self.TEXT_COLOR)
        self.screen.blit(result_surface, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
