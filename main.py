import random
import pygame
import time
import generator

pygame.init()

# Define the dimensions of the game window
window_width = 1200
window_height = 800
screen = pygame.display.set_mode((window_width,window_height))
# Initialise the game window
window = pygame.display.set_mode((window_width, window_height))

# Define the colours
black = (0,0,0)
white = (255,255,255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Create a list of the colours
colours = [blue, red, yellow, green]

# Define the font used in the game
font = pygame.font.Font(None, 32)

# Create a list of the circles
circles = []
for i, colour in enumerate(colours):
    x = 100 + i * 100
    y = 200
    r = 50
    circles.append(pygame.draw.circle(screen, colour, (x, y), r))

# Load the map from the file
from map import World_Map

# Load the start background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (window_width, window_height))

# Load the heart image
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (50, 50))

# Load the enemy image
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (40, 40))

# Load level 1 image
lvl1 = pygame.image.load("background_lvl1.png")
lvl1 = pygame.transform.scale(lvl1, (window_width, window_height))
lvl1 = pygame.transform.scale(lvl1, (1835, 1250))

dino_image = pygame.image.load("Dino1.gif")
dino_image = pygame.transform.scale(dino_image, (70, 70))

dino_image2 = pygame.image.load("Dino2.gif")
dino_image2 = pygame.transform.scale(dino_image2, (70, 70))

dino_image3 = pygame.image.load("Dino3.gif")
dino_image3 = pygame.transform.scale(dino_image3, (70, 70))

dino_image4 = pygame.image.load("Dino4.gif")
dino_image4 = pygame.transform.scale(dino_image4, (70, 70))

fps = 30
frame_duration = 1000 / fps
frame_time = 0

# Initialise Player & Enemy
player = generator.Player(0,0,dino_image)
enemy = generator.Enemy(0,0,enemy_image)

# Find the starting position of the player in the map
for row_index, row in enumerate(World_Map):
    if "p" in row:
        player.rect.x = row.index("p") * 40
        player.rect.y = row_index * 40

# Set the title of the window
pygame.display.set_caption("2D World Exploring Game")

# load music file
pygame.mixer.music.load("Background Music.mp3")

# play music
pygame.mixer.music.play()
pygame.mixer.music.play(-1)

# Start the game loop
game_over = False
start_screen = True

# Start screen
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_screen = False

    # Draw the background image
    screen.blit(background, (0, 0))

    # Flash the "Start" text
    if int(time.time() * 3) % 2 == 0:
        text = font.render("Press Space to Start", True, white)
        text_rect = text.get_rect()
        text_x = window_width // 2 - text_rect.width // 2
        text_y = window_height // 2 - text_rect.height // 2
        screen.blit(text, [text_x, text_y])

    pygame.display.update()

# Define the circle properties
circle_width = 200
circle_height = 200
circle_positions = [(250, 400), (450, 400), (650, 400), (850, 400)]
circles = [pygame.Rect(x, y, circle_width, circle_height) for x, y in circle_positions]
characters = [dino_image,dino_image2, dino_image3, dino_image4]

# Define the text position
font = pygame.font.Font(None, 52)
text_x = window_width / 2
text_y = 300

screen.blit(background, (0, 0))

# Variable to store the selected colour
selected_colour = None

# Define the flash rate (in milliseconds)
flash_rate = 500
current_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # Get the mouse position
            x, y = pygame.mouse.get_pos()
            # Check if the mouse is over one of the circles
            for i, circle in enumerate(circles):
                if circle.collidepoint(x, y):
                    selected_colour = colours[i]
                    running = False

    # Clear the screen
    screen.blit(background, (0, 0))

    # Flashing "Select Character"
    if (pygame.time.get_ticks() // flash_rate) % 2 == 0:
        text = font.render("Select Character", True, white)
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)

    # Draw the circles
    for i in range(4):
        screen.blit(characters[i],circle_positions[i])

    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.quit()

max ={blue: 20, red: 20, yellow: 20, green: 13}
colour_map = {(0, 255, 0): "green", (0, 0, 255): "blue", (255, 0, 0): "red", (255, 255, 0): "yellow"}
frames = []

for x in range(0,max[selected_colour]):
    image = "{}_{:02d}_delay-0.1s.gif".format(colour_map[selected_colour], x)
    animation = pygame.image.load(image)
    frames.append(pygame.transform.scale(animation, (40, 40)))

clock = pygame.time.Clock()
frame_index = 0
count = 0

pygame.init()
screen = pygame.display.set_mode((window_width,window_height))
# Initialise the game window
window = pygame.display.set_mode((window_width, window_height))
# Set the title of the window
pygame.display.set_caption("Dino Dash 'n Blast")

enemies = pygame.sprite.Group()
left = False

fireballs = []
generator.Fireball.image = pygame.transform.scale(pygame.image.load("fireball.png"), (20, 20))

# load the background music and sound effect
background_music = pygame.mixer.Sound("Background Music.mp3")
fireball_sound = pygame.mixer.Sound("fireball.mp3")

# start the clock
start_time = pygame.time.get_ticks()

# define the spawn threshold
spawn_threshold = 500

# play the background music in a loop
background_music.play(-1)
enemies = generator.create_enemies(World_Map, enemy_image, pygame.time.get_ticks() - start_time)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True


    # Get the key presses from the user
    keys = pygame.key.get_pressed()

    player.image = frames[frame_index]
    # Update the frame index
    if count % 5 == 0:
        frame_index = (frame_index + 1) % len(frames)

    # Store the original player position
    original_player_x = player.rect.x
    original_player_y = player.rect.y
    print("orignal" + str(original_player_x) +" "+ str(original_player_y))

    # Move the player in the specified direction
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.rect.y -= player.move
        if len(fireballs) != 0:
            for fire in fireballs:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    fire.y += 5
                else:
                    fire.y += 3
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.rect.y += player.move
        if len(fireballs) != 0:
            for fire in fireballs:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    fire.y -= 5
                else:
                    fire.y -= 3
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.rect.x -= player.move
        left = True
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.rect.x += player.move
        left = False
    else:
        player.image = frames[0]

    if keys[pygame.K_l]:
        player.health = 0

    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        player.move = 5
    else:
        player.move = 3

    if keys[pygame.K_SPACE]:
        fireball_sound.play()

        fireball = generator.Fireball(window_width // 2, window_height // 2)
        fireballs.append(fireball)
        if left:
            fireball.image = pygame.transform.flip(generator.Fireball.image, True, False)
            fireball.direction = -1
        else:
            fireball.image = generator.Fireball.image
            fireball.direction = 1

    # Define the camera offset based on the player's position
    camera_offset_x = -player.rect.x + window_width // 2
    camera_offset_y = -player.rect.y + window_height // 2

    print("camera_off" + str(camera_offset_x) + " " + str(camera_offset_y))

    # Clear the game window
    screen.blit(background, (0, 0))

    # Draw the background image
    screen.blit(lvl1, (camera_offset_x, camera_offset_y))

    #for enemy in enemies:
     #   enemy.draw(screen)
      #  print("im bein printed bukko")

    for enemy in enemies:
        enemy.move_towards_player(player)
        if enemy.health == 0:
            enemies.remove(enemy)
            print("ded")
        if player.rect.x - window_width // 2 <= enemy.rect.x <= player.rect.x + window_width // 2:
            print("passed 1")
            if player.rect.y - window_height // 2 <= enemy.rect.y <= player.rect.y + window_height // 2:
                di = enemy.rect.x - (player.rect.x - window_width // 2)
                ck = enemy.rect.y - (player.rect.y - window_height // 2)
                screen.blit(enemy.image, (di,ck))
                print("IM ON THE SCREEN BAYBEEEEEE")

    if left:
        player.image = pygame.transform.flip(player.image, True, False)

    for fireball in fireballs:
        fireball.x += fireball.speed * fireball.direction
        if fireball.x > window_width or fireball.x < 0:
            fireballs.remove(fireball)
    for fireball in fireballs:
        for enemy in enemies:
            if pygame.Rect(fireball.x, fireball.y, 20, 20).colliderect(pygame.Rect(enemy.rect.x, enemy.rect.y, 32, 32)):
                fireballs.remove(fireball)
                enemy.health -= 1
                break
        screen.blit(fireball.image, (fireball.x, fireball.y))

    # Draw player
    screen.blit(player.image,(window_width // 2, window_height // 2))

    print("final" + str(window_width // 2) + " " + str(window_height // 2))



    # Check if the player has collided with the walls and enemies
    for row_index, row in enumerate(World_Map):
        for col_index, col in enumerate(row):
            x = col_index * 40
            y = row_index * 40
            if col == "x" and player.rect.x + 30 > x and player.rect.x < x + 40 and player.rect.y + 30 > y and player.rect.y < y + 40:
                player.rect.x = original_player_x
                player.rect.y = original_player_y
            elif col == "e" and player.rect.x + 30 > x and player.rect.x < x + 40 and player.rect.y + 30 > y and player.rect.y < y + 40:
                player.rect.x = original_player_x
                player.rect.y = original_player_y


    # Draw Hearts
    generator.draw_hearts(screen, player.health, heart_image)

    clock.tick(fps)
    count += 1
    if player.health == 0:
        game_over = True
    # Update the game window
    pygame.display.update()

# Quit pygame
pygame.quit()

pygame.init()
screen = pygame.display.set_mode((window_width,window_height))
# Initialise the game window
window = pygame.display.set_mode((window_width, window_height))
# Define the font used in the game
font = pygame.font.Font(None, 32)
# Set the title of the window
pygame.display.set_caption("Dino Dash 'n Blast")

end = True
while end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False

    # Draw the background image
    screen.blit(background, (0, 0))

    # Flash the "Start" text
    if int(time.time() * 3) % 2 == 0:
        text = font.render("Game Over", True, white)
        text_rect = text.get_rect()
        text_x = window_width // 2 - text_rect.width // 2
        text_y = window_height // 2 - text_rect.height // 2
        screen.blit(text, [text_x, text_y])

    pygame.display.update()
# Quit the game
pygame.quit()
