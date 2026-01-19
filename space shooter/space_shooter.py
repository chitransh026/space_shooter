
import pygame
from random import randint
pygame.mixer.init()

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

# Load assets
player_surf = pygame.image.load('player.png').convert_alpha()
player_rect = player_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100))
player_speed = 7

background_surf = pygame.image.load('background.jpg').convert_alpha()
meteor_surf = pygame.image.load('meteor.png').convert_alpha()
laser_surf = pygame.image.load('laser.png').convert_alpha()

# Font for menu and score
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 40)

# Game variables
background_y = 0
background_speed = 3
meteor_speed = 5
laser_speed = 30
score = 0
running = True

# State management
game_active = False  # Start with the menu
laser_active = False

# Initialize meteor positions
meteor_rects = [meteor_surf.get_rect(center=(randint(0, WINDOW_WIDTH), randint(-100, -40))) for _ in range(5)]


def reset_game():
    # Reset game variables for a fresh start.
    global player_rect, meteor_rects, laser_active, score, background_y
    player_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100)
    meteor_rects = [meteor_surf.get_rect(center=(randint(0, WINDOW_WIDTH), randint(-100, -40))) for _ in range(5)]
    laser_active = False
    score = 0
    background_y = 0


def display_text(text, font, color, center):
    # Helper function to display centered text.
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=center)
    display_surface.blit(text_surf, text_rect)


while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_active:
            # Start or restart game on keypress
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                reset_game()

        if game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not laser_active:
            # Fire laser
            laser_rect = laser_surf.get_rect(midbottom=(player_rect.centerx, player_rect.top))
            laser_active = True

    # Game logic when active
    if game_active:
        # Handle player movement (restrict to horizontal only)
        pygame.mixer.music.load('game_music.wav')
        pygame.mixer.music.set_volume(0.3)  # Adjust volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play the music in an infinite loop
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
            player_rect.x += player_speed

        # Scroll background
        background_y += background_speed
        background_y %= WINDOW_HEIGHT
        display_surface.blit(background_surf, (0, background_y - WINDOW_HEIGHT))
        display_surface.blit(background_surf, (0, background_y))

        # Move meteors
        for meteor_rect in meteor_rects:
            meteor_rect.y += meteor_speed
            if meteor_rect.top > WINDOW_HEIGHT:
                meteor_rect.center = (randint(0, WINDOW_WIDTH), randint(-100, -40))
            display_surface.blit(meteor_surf, meteor_rect)

        # Laser movement
        if laser_active:
            pygame.mixer.music.load('laser.wav')
            pygame.mixer.music.set_volume(0.3)
            laser_rect.y -= laser_speed
            display_surface.blit(laser_surf, laser_rect)
            if laser_rect.bottom < 0:  # Deactivate laser if it goes off-screen
                laser_active = False

        # Collision detection: Laser and meteors
        for meteor_rect in meteor_rects:
            if laser_active and laser_rect.colliderect(meteor_rect):
                meteor_rect.center = (randint(0, WINDOW_WIDTH), randint(-100, -40))  # Reset meteor
                laser_active = False
                score += 1  # Increase score on successful hit

        # Collision detection: Player and meteors
        for meteor_rect in meteor_rects:
            if player_rect.colliderect(meteor_rect):
                game_active = False  # End game on collision

        # Draw player and score
        display_surface.blit(player_surf, player_rect)
        score_surf = small_font.render(f"Score: {score}", True, (255, 255, 255))
        display_surface.blit(score_surf, (10, 10))

    else:
        # Display start or game over screen
        display_surface.fill('black')
        if score == 0:
            display_text("SPACE SHOOTER", font, (255, 255, 255), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))
            display_text("Press ENTER to Start", small_font, (255, 255, 255), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        else:
            display_text("GAME OVER", font, (255, 255, 255), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))
            display_text(f"Final Score: {score}", small_font, (255, 255, 255), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            display_text("Press ENTER to Restart", small_font, (255, 255, 255), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.5))

    pygame.display.update()

pygame.quit()

