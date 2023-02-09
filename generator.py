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
    def move_towards_player(self, Player, death):
        a = Player.rect.x + 20
        b = Player.rect.y + 40
        # Calculate the distance between the enemy and the player
        dx = self.rect.x - a
        dy = self.rect.y - b
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5

        # If the distance is less than 900 pixels, move the enemy towards the player
        if distance < 900:
            dx = min(max(dx, -1), 1)
            dy = min(max(dy, -1), 1)

            self.rect.x -= dx
            self.rect.y -= dy
        death = self.health_check(Player, death)
        return death

    def health_check(self, Player, death):
        a = Player.rect.x + 20
        b = Player.rect.y + 40
        if self.rect.x == a and self.rect.y == b:
            self.health -= 1
            Player.health -= 1
            Player.rect.x += 5
            Player.rect.y += 5
            death += 1
        return death

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        print(self.rect)

class Fireball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.direction = 1
        self.image = pygame.transform.scale(pygame.image.load("fireball.png"), (20, 20))

def create_enemies(World_Map, enemy_image):
    enemies = pygame.sprite.Group()
    ran = [True, False]
    for y, row in enumerate(World_Map):
        for x, char in enumerate(row):
            # Position calculation based on the dimensions of the enemy sprite
            # and the size of the cells in the World_Map
            if char == "v" and np.random.choice(ran, p=[3/46, 43/46]):
                enemies.add(Enemy(x*40 + 20, y*40 + 20, enemy_image))
    for enemy in enemies:
        enemy.health = 1
    return enemies

def draw_hearts(screen, player_health, heart_image):
    for i in range(player_health):
        screen.blit(heart_image, (10 + i * 30, 10))
