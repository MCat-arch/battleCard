# merge.py
from card import Card

class Merge:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

    def handle_merge(self):
        """Tangani merge kartu dengan level yang sama."""
        cards_by_name = {}
        for card in self.player.cards:
            if card.name in cards_by_name:
                cards_by_name[card.name].append(card)
            else:
                cards_by_name[card.name] = [card]

        for name, cards in cards_by_name.items():
            if len(cards) >= 2:
                new_card = Card(f"{name}+", cards[0].hp * 2, cards[0].atk * 2)
                self.player.cards.remove(cards[0])
                self.player.cards.remove(cards[1])
                self.player.add_card(new_card)
                break
