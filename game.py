import pygame
import os

pygame.font.init()

# Define constants for the game window
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define constants for the spaceships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
MAX_BULLETS = 3  # Maximum number of bullets each player can have
BULLET_VEL = 7
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)  # Create a border in the middle

# Define game-related constants
VEL = 5  # Spaceship movement speed
FPS = 60  

# Define fonts for health and winner display
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Define custom events for handling hits
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

pygame.init()

# Create the game window
DIS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ranger")

# Function to draw the winner text
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    DIS.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

# Function to draw the game display
def open_display(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health):
    DIS.blit(SPACE, (0, 0))
    pygame.draw.rect(DIS, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE)
    DIS.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    DIS.blit(yellow_health_text, (10, 10))

    DIS.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    DIS.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(DIS, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(DIS, YELLOW, bullet)

    pygame.display.update()

# Function to handle yellow spaceship movement
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Move left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Move right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Move up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # Move down
        yellow.y += VEL

# Function to handle red spaceship movement
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Move left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Move right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Move up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # Move down
        red.y += VEL

# Function to handle bullets and collisions
def handle_bullets(red, yellow, red_bullets, yellow_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# Main game loop
def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    run = True
    clock = pygame.time.Clock()  # Create a clock object for controlling frame rate

    yellow_bullets = []  # List to store yellow bullets
    red_bullets = []  # List to store red bullets

    yellow_health = 10  # Initialize yellow's health
    red_health = 10  # Initialize red's health

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and len(yellow_bullets) < MAX_BULLETS:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)  # Display the winner and end the game
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(red, yellow, red_bullets, yellow_bullets)

        open_display(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health)

        pygame.display.update()
        clock.tick(FPS)  # Limit the frame rate to 60 frames per second

    # Restart the game
    main()

if __name__ == "__main__":
    main()
