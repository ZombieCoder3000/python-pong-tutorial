import pygame
import sys
import random

# ---------------------------------------------------------
# Section: The Setup
# ---------------------------------------------------------
# We start by importing the necessary libraries and setting
# up the game window and clock.

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong - DevWithH')

# ---------------------------------------------------------
# Section: The Shapes
# ---------------------------------------------------------
# Here we define our game objects (Rectangles) and the
# variables that will control their speed later.

# Game Rectangles: Rect(x, y, width, height)
ball = pygame.Rect(SCREEN_WIDTH/2 - 15, SCREEN_HEIGHT/2 - 15, 30, 30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT/2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT/2 - 70, 10, 140)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Game Variables (Speed)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# ---------------------------------------------------------
# Section: Movement & Bouncing
# ---------------------------------------------------------
# These functions handle the physics. We need to define
# these BEFORE the main loop for the code to run.

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    
    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Boundary Collision (Top and Bottom)
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Score Logic (Left and Right)
    if ball.left <= 0:
        player_score += 1
        ball_restart()
        
    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1
        ball_restart()

    # Paddle Collision
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    # Prevent paddle from going off screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

# ---------------------------------------------------------
# Section: The AI & Scoring
# ---------------------------------------------------------
# The logic to make the opponent move automatically.

def opponent_ai():
    # Simple AI: Opponent moves towards the ball
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
        
    # Prevent AI from going off screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

# ---------------------------------------------------------
# Section: The Main Loop & Drawing
# ---------------------------------------------------------
# This is the heartbeat of the game. It handles input,
# clears the screen, and draws our shapes every frame.

while True:
    # 1. Handling Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Key Checks (Player Movement)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # 2. Logic Calls
    ball_animation()
    player_animation()
    opponent_ai()

    # 3. Visuals (Drawing)
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))

    # Drawing Score
    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (600, 470))

    # 4. Updating the window
    pygame.display.flip()
    clock.tick(60)