import random 
import pygame
from abc import ABC, abstractmethod
#Versi 0.3
class Card(ABC):
    @abstractmethod
    def __init__(self, name, attack, defense, health, level, price, img_link):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.level = level
        self.price = price
        self.img_link = img_link
        self.image = pygame.image.load(img_link) 
        self.image = pygame.transform.scale(self.image, (150, 200))
        self.set_base_stats(self.attack, self.defense, self.health)
        
    @abstractmethod
    def set_base_stats(self):
        pass
    
    @abstractmethod
    def special_ability(self):
        pass
    
    def upgrade(self):
        self.level += 1
        self.attack += self.attack_growth
        self.defense += self.defense_growth if self.defense <= 0.9 else 0
        self.health += self.health_growth
        print(f"{self.name} has been merged and upgraded to level {self.level}!")
        print(f"New stats - Attack: {self.attack}, Defense: {self.defense:.2f}, Health: {self.health}")

    def take_damage(self, damage):
        actual_damage = damage * (1 - self.defense)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} received {actual_damage:.2f} damage, remaining health: {self.health:.2f}")
        
    def is_alive(self):
        return self.health > 0

    def calculate_power(self):
        return (self.attack * self.attack_multiplier + 
                self.defense * self.defense_multiplier) * self.level
    
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health

#Class untuk kartu karakter
class Warrior(Card):
    def __init__(self, name, attack, defense, health, level, price, link):
        super().__init__(name, attack, defense, health, level, price, link)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 6
        self.defense_growth = 0.05
        self.health_growth = 25
        self.attack_multiplier = 1.2
        self.defense_multiplier = 0.8
        
    def special_ability(self):
        return self.attack * (1 + (1 - self.health/90) * 0.5)

class Archer(Card):
    def __init__(self, name, attack, defense, health, level, price, link):
        super().__init__(name, attack, defense, health, level, price, link)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 8
        self.defense_growth = 0.03
        self.health_growth = 15
        self.attack_multiplier = 1.5
        self.defense_multiplier = 0.5
        
    def special_ability(self):
        return self.attack * 2 if random.random() < 0.3 else self.attack

class Guardian(Card):
    def __init__(self, name, attack, defense, health, level, price, link):
        super().__init__(name, attack, defense, health, level, price, link)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 4
        self.defense_growth = 0.07
        self.health_growth = 35
        self.attack_multiplier = 0.8
        self.defense_multiplier = 1.2
        
    def special_ability(self):
        return self.defense * 10

class Assassin(Card):
    def __init__(self, name, attack, defense, health, level, price, link):
        super().__init__(name, attack, defense, health, level, price, link)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 9
        self.defense_growth = 0.02
        self.health_growth = 12
        self.attack_multiplier = 1.7
        self.defense_multiplier = 0.3
        
    def special_ability(self):
        return self.attack * 3 if random.random() < 0.2 else self.attack
