import pygame
import random

# Define color constants
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Initialize Pygame and font
pygame.init()
font_game = pygame.font.SysFont("Ubuntu", 40)

# Game settings
FRAME_DELAY = 30
PADDLE_SPEED = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Player positions
player1_x = 10
player1_y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2
player2_x = SCREEN_WIDTH - PADDLE_WIDTH - 10
player2_y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2

# Player scores
score_player1 = 0
score_player2 = 0

# Player movement flags
move_player1_up = False
move_player1_down = False
move_player2_up = False
move_player2_down = False

# Ball position and velocity
ball_x = SCREEN_WIDTH / 2
ball_y = SCREEN_HEIGHT / 2
BALL_SIZE = 8
ball_velocity_x = -10
ball_velocity_y = random.choice([-5, 5])

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_objects():
    # Draw paddles and ball
    pygame.draw.rect(screen, COLOR_WHITE, (int(player1_x), int(player1_y), PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, COLOR_WHITE, (int(player2_x), int(player2_y), PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, COLOR_WHITE, (int(ball_x), int(ball_y)), BALL_SIZE)
    score_text = font_game.render(f"{score_player1} - {score_player2}", False, COLOR_WHITE)
    screen.blit(score_text, (SCREEN_WIDTH / 2 - score_text.get_width() / 2, 30))

def apply_player_movement():
    global player1_y
    global player2_y

    if move_player1_up:
        player1_y = max(player1_y - PADDLE_SPEED, 0)
    if move_player1_down:
        player1_y = min(player1_y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
    if move_player2_up:
        player2_y = max(player2_y - PADDLE_SPEED, 0)
    if move_player2_down:
        player2_y = min(player2_y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)

def apply_ball_movement():
    global ball_x
    global ball_y
    global ball_velocity_x
    global ball_velocity_y
    global score_player1
    global score_player2

    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Ball collision with top and bottom walls
    if ball_y - BALL_SIZE <= 0 or ball_y + BALL_SIZE >= SCREEN_HEIGHT:
        ball_velocity_y = -ball_velocity_y

    # Ball collision with paddles
    if (ball_x - BALL_SIZE <= player1_x + PADDLE_WIDTH and
        player1_y <= ball_y <= player1_y + PADDLE_HEIGHT):
        ball_velocity_x = -ball_velocity_x
        ball_velocity_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    elif (ball_x + BALL_SIZE >= player2_x and
          player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
        ball_velocity_x = -ball_velocity_x
        ball_velocity_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

    # Ball goes out of bounds
    if ball_x - BALL_SIZE <= 0:
        score_player2 += 1
        reset_ball()
    elif ball_x + BALL_SIZE >= SCREEN_WIDTH:
        score_player1 += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y
    ball_x = SCREEN_WIDTH / 2
    ball_y = SCREEN_HEIGHT / 2
    ball_velocity_x = random.choice([-10, 10])
    ball_velocity_y = random.choice([-5, 5])

# Set window title and fill initial screen
pygame.display.set_caption("Pong Game")
screen.fill(COLOR_BLACK)
pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                move_player1_up = True
            if event.key == pygame.K_s:
                move_player1_down = True
            if event.key == pygame.K_UP:
                move_player2_up = True
            if event.key == pygame.K_DOWN:
                move_player2_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move_player1_up = False
            if event.key == pygame.K_s:
                move_player1_down = False
            if event.key == pygame.K_UP:
                move_player2_up = False
            if event.key == pygame.K_DOWN:
                move_player2_down = False

    screen.fill(COLOR_BLACK)
    apply_player_movement()
    apply_ball_movement()
    draw_objects()
    pygame.display.flip()
    pygame.time.wait(FRAME_DELAY)

pygame.quit()
