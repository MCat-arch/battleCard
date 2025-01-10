import pygame
import sys
import random
# from input_name import get_player_names
from battlefield import PreBattle, GameObject, Battle
from deck import Deck
from card import Card, Warrior, Archer, Assassin, Guardian

list_card = [
            Warrior("Warrior", 15, 0.3, 90, 1, 6, "assets/card.png"),
            Archer("Archer", 12, 0.2, 70, 1, 6, "assets/card.png"),
            Guardian("Guardian", 15, 0.6, 130, 1, 6, "assets/card.png"),
            Assassin("Assassin", 28, 0.25, 75, 1, 6, "assets/card.png"),
]


class Dashboard(GameObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.BG_IMAGE_PATH = "assets/mainmenu.png"
        self.TITLE_COLOR = (50, 50, 50)
        self.HOVER_COLOR = (50, 50, 150)
        # Muat gambar latar belakang
        try:
            self.bg_image = pygame.image.load(self.BG_IMAGE_PATH)
            self.bg_image = pygame.transform.scale(self.bg_image, screen.get_size())  # Sesuaikan ukuran gambar dengan layar
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            sys.exit()
        #input music
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music1.mp3")  
        pygame.mixer.music.play(-1)

        self.buttons = [
            {"text": "Start Game", "pos": (640, 300)},
            {"text": "Settings", "pos": (640, 400)},
            {"text": "Exit", "pos": (640, 500)},
        ]

    def show_dashboard(self):
        while True:
            self.screen.blit(self.bg_image, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            self.font_title = pygame.font.Font(None, 80)
            title_surface = self.font_title.render("BATTLE CARD", True, self.TITLE_COLOR)
            title_rect = title_surface.get_rect(center=(640, 100))
            self.screen.blit(title_surface, title_rect)

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
            rounds = 0
            # Mulai pertempuran di Battlefield
            battlefield = PreBattle(self.screen, [first_player, second_player])
            battlefield.start_battlefield()
            

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.main_card = []
        self._coins = 100  # Encapsulated attribute
        self._score = 0    # Encapsulated attribute

    # Getter and setter methods for coins
    def get_coins(self):
        return self._coins

    def set_coins(self, coins):
        if coins >= 0:
            self._coins = coins
        else:
            print("Coins cannot be negative")

    # Getter and setter methods for score
    def get_score(self):
        return self._score

    def set_score(self, score):
        if score >= 0:
            self._score = score
        else:
            print("Score cannot be negative")


def get_player_names(screen):
    pygame.init()
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()
    
    BG_IMAGE_PATH = "assets/mainmenu.png"
    TEXT_COLOR = (50, 50, 50)
    TEXT_COLOR_SUBMIT = (255, 255, 255)
    INPUT_COLOR = (50, 50, 150)
    ACTIVE_COLOR = (100, 100, 250)
    try:
        bg_image = pygame.image.load(BG_IMAGE_PATH)
        bg_image = pygame.transform.scale(bg_image, screen.get_size())  # Sesuaikan ukuran gambar dengan layar
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit()
    screen_width, screen_height = screen.get_size()

    input_boxes = [
        {"text": "Player 1 Name: ", "rect": pygame.Rect(0, 0, 400, 50), "value": ""},
        {"text": "Player 2 Name: ", "rect": pygame.Rect(0, 0, 400, 50), "value": ""},
    ]

    # Posisi awal vertikal
    vertical_offset = (screen_height - (len(input_boxes) * 100 + 50)) // 2
    for idx, box in enumerate(input_boxes):
        box["rect"].x = (screen_width - box["rect"].width) // 2
        box["rect"].y = vertical_offset + idx * 100

    # Posisi tombol "Submit"
    submit_button = {"text": "Submit", "rect": pygame.Rect(0, 0, 200, 50)}
    submit_button["rect"].x = (screen_width - submit_button["rect"].width) // 2
    submit_button["rect"].y = input_boxes[-1]["rect"].y + 100

    active_box = None

    while True:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Render kotak input
        for idx, box in enumerate(input_boxes):
            label_surface = font.render(box["text"], True, TEXT_COLOR)
            label_x = box["rect"].x
            label_y = box["rect"].y - 30
            screen.blit(label_surface, (label_x, label_y))

            color = ACTIVE_COLOR if idx == active_box else INPUT_COLOR
            pygame.draw.rect(screen, color, box["rect"], 2)

            # Render teks di kotak input
            text_surface = font.render(box["value"], True, TEXT_COLOR)
            screen.blit(text_surface, (box["rect"].x + 10, box["rect"].y + 10))

        # Tampilkan tombol "Submit"
        pygame.draw.rect(screen, INPUT_COLOR, submit_button["rect"])
        submit_text = font.render(submit_button["text"], True, TEXT_COLOR_SUBMIT)
        submit_text_x = submit_button["rect"].x + (submit_button["rect"].width - submit_text.get_width()) // 2
        submit_text_y = submit_button["rect"].y + (submit_button["rect"].height - submit_text.get_height()) // 2
        screen.blit(submit_text, (submit_text_x, submit_text_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button["rect"].collidepoint(mouse_pos):
                    if all(box["value"] for box in input_boxes):
                        return input_boxes[0]["value"], input_boxes[1]["value"]
                for idx, box in enumerate(input_boxes):
                    if box["rect"].collidepoint(mouse_pos):
                        active_box = idx
                        break
            elif event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["value"] = input_boxes[active_box]["value"][:-1]
                elif event.key == pygame.K_RETURN:
                    active_box = None
                else:
                    input_boxes[active_box]["value"] += event.unicode

        clock.tick(30)
 