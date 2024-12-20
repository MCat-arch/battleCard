import pygame
import sys

def get_player_names(screen):
    pygame.init()
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    BG_COLOR = (20, 20, 20)
    TEXT_COLOR = (255, 255, 255)
    INPUT_COLOR = (50, 50, 150)
    ACTIVE_COLOR = (100, 100, 250)

    input_boxes = [
        {"text": "Player 1 Name: ", "rect": pygame.Rect(200, 200, 400, 50), "value": ""},
        {"text": "Player 2 Name: ", "rect": pygame.Rect(200, 300, 400, 50), "value": ""},
    ]

    active_box = None

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Render kotak input
        for idx, box in enumerate(input_boxes):
            label_surface = font.render(box["text"], True, TEXT_COLOR)
            screen.blit(label_surface, (box["rect"].x, box["rect"].y - 30))

            color = ACTIVE_COLOR if idx == active_box else INPUT_COLOR
            pygame.draw.rect(screen, color, box["rect"], 2)

            # Render teks di kotak input
            text_surface = font.render(box["value"], True, TEXT_COLOR)
            screen.blit(text_surface, (box["rect"].x + 10, box["rect"].y + 10))

        # Tampilkan tombol "Submit"
        submit_button = {"text": "Submit", "rect": pygame.Rect(300, 400, 200, 50)}
        pygame.draw.rect(screen, INPUT_COLOR, submit_button["rect"])
        submit_text = font.render(submit_button["text"], True, TEXT_COLOR)
        screen.blit(submit_text, submit_button["rect"].move(40, 10))

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
