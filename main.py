import pygame

import random
import math

from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# background Sound
mixer.music.load("background.wav")
mixer.music.play(-1) #by initializing the value to -1 the music will play in loop

# title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# main Player
playerImg = pygame.image.load('gunship.png')
playerX = 370 #initial position of main player(gunship)
playerY = 500 #initial position of main player(gunship)
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# for loop to create multiple enemies (num_of_enemies)
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736)) #-random values of x coordinates using "random" module
    enemyY.append(random.randint(50, 150)) #-random values of y coordinates using "random" module
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500  #initial position of bullet at y-axis
bulletX_change = 0
bulletY_change = 5

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# function to show score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# function to show the game over screen
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# function to display and set player at position
def player(x, y):
    screen.blit(playerImg, (x, y))

# function to display and set enemy at position
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# function to display and fire a bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# function to detect weather the bullet collided with the enemy
# using the formula of ditance between two points
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

# for running the screen
running = True
while running:

    # setting background color - RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP: #KEYUP detects weather a key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change

    # to stop the player from leaving the window boundary(800x600)
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
         # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        # to stop the enemy from leaving the window boundary(800x600)
        # and to also move the enemy from left to right when it hits the boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 1 #when x- touches 0 move right
            enemyY[i] += enemyY_change[i] #this will make enemy move down
        
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1 #when y- touches 736 move left
            enemyY[i] += enemyY_change[i] #this will make enemy move down

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY) #stores the True/False of collision
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 500 # reset the position of bullet to 500(initial point)
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
