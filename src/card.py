class Card:
    def __init__(self, name, health, attack, price, level=1):
        """
        Initialize the card with attributes:
        - name: Name of the card
        - hp: Health points of the card
        - atk: Attack points of the card
        - price: Price of the card
        """
        self.name = name
        self.health = health
        self.attack = attack
        self.price = price

    def __str__(self):
        """
        String representation of the card for debugging or card information.
        """
        return f"Card(name={self.name}, hp={self.hp}, atk={self.atk}, price={self.price})"

    def attack(self, other_card):
        """
        Simulate an attack on another card.
        - Reduces the HP of the other card by the ATK of this card.
        """
        if not isinstance(other_card, Card):
            raise ValueError("Target must be an instance of Card.")
        other_card.hp -= self.atk

    def is_alive(self):
        """
        Check if the card is still alive (HP > 0).
        """
        return self.hp > 0