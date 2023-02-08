import pygame
import math
import numpy as np

class Player:
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.move = 3 # Define the movement speed of the player
        self.rect.x = x
        self.rect.y = y
        self.health = 5

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def decrease_hearts(self):
        self.hearts -= 1

    def get_position(self):
        return (self.x, self.y)

    def get_hearts(self):
        return self.hearts


# Class for the enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.health = 1

    # Method to move the enemy towards the player
    def move_towards_player(self, Player):
        # Calculate the distance between the enemy and the player
        distance = ((self.rect.x - Player.rect.x) ** 2 + (self.rect.y - Player.rect.y) ** 2) ** 0.5

        # If the distance is less than 20 pixels, move the enemy towards the player
        if distance < 20:
            angle = math.atan2(Player.rect.y - self.rect.y, Player.rect.x - self.rect.x)
            self.rect.x += math.cos(angle)
            self.rect.y += math.sin(angle)

    def update(self, Player):
        if abs(self.x - Player.rect.x) <= 2 and abs(self.y - Player.rect.y) <= 2:
            if Player.rect.x > self.x:
                self.x += 1
            elif Player.rect.x < self.x:
                self.x -= 1
            if Player.rect.y > self.y:
                self.y += 1
            elif Player.rect.y < self.y:
                self.y -= 1
            if self.x == Player.rect.x and self.y == Player.rect.y:
                self.hearts -= 1
                Player.hearts -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fireball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.direction = 1
        self.image = pygame.transform.scale(pygame.image.load("fireball.png"), (20, 20))

def create_enemies(World_Map, enemy_image, time):
    enemies = pygame.sprite.Group()
    ran = [True, False]
    for y, row in enumerate(World_Map):
        for x, char in enumerate(row):
            # Position calculation based on the dimensions of the enemy sprite
            # and the size of the cells in the World_Map
            if char == "v" and np.random.choice(ran, p=[0.1 + (time // 1000000000), 0.9 - (time // 1000000000)]):
                enemies.add(Enemy(x*40 + 20, y*40 + 20, enemy_image))
    return enemies

def draw_hearts(screen, player_health, heart_image):
    for i in range(player_health):
        screen.blit(heart_image, (10 + i * 30, 10))



