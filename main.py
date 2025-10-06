import pygame
import sys
import os
import random
from src.player import Player
from src.enemy import Enemy
from collectible import Collectible

# --- Asset Setup ---
SOUNDS_DIR = "sounds"
SPRITES_DIR = "sprites"
os.makedirs(SOUNDS_DIR, exist_ok=True)
os.makedirs(SPRITES_DIR, exist_ok=True)

def create_placeholder_audio(filename):
    path = os.path.join(SOUNDS_DIR, filename)
    if not os.path.exists(path):
        if filename.endswith('.wav'):
            with open(path, 'wb') as f:
                f.write(b'RIFF$\x00\x00\x00WAVEfmt ' + b'\x10\x00\x00\x00\x01\x00\x01\x00' +
                        b'\x40\x1f\x00\x00\x80>\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
        elif filename.endswith('.mp3'):
            with open(path, 'wb') as f:
                f.write(b'ID3\x03\x00\x00\x00\x00\x00\x21')

def create_placeholder_sprite(filename, color):
    path = os.path.join(SPRITES_DIR, filename)
    if not os.path.exists(path):
        pygame.init()
        surf = pygame.Surface((48, 48), pygame.SRCALPHA)
        surf.fill(color)
        pygame.image.save(surf, path)

def create_placeholder_bg(filename):
    path = os.path.join(SPRITES_DIR, filename)
    if not os.path.exists(path):
        pygame.init()
        surf = pygame.Surface((800, 600))
        surf.fill((40, 60, 120))
        for i in range(0, 800, 80):
            pygame.draw.line(surf, (60, 80, 160), (i, 0), (i, 600), 2)
        for j in range(0, 600, 80):
            pygame.draw.line(surf, (60, 80, 160), (0, j), (800, j), 2)
        pygame.image.save(surf, path)

create_placeholder_audio("background_music.mp3")
create_placeholder_audio("collision.wav")
create_placeholder_audio("collect.wav")
create_placeholder_sprite("player.png", (0, 200, 255, 255))        # Blue for player
create_placeholder_sprite("enemy.png", (255, 50, 50, 255))         # Red for enemy
create_placeholder_sprite("collectible.png", (255, 215, 0, 255))   # Gold for collectible
create_placeholder_bg("background.png")

# --- Initialize pygame and mixer ---
pygame.init()
pygame.mixer.init()

# --- Load sounds ---
pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background_music.mp3"))
collision_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "collision.wav"))
collect_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "collect.wav"))

# --- Game setup ---
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Awesome Game")

bg_image = pygame.image.load(os.path.join(SPRITES_DIR, "background.png"))

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# --- Menu logic ---
def main_menu():
    options = ["Start Game", "Quit"]
    selected = 0
    title_text = big_font.render("My Awesome Game", True, (255, 255, 255))
    blink = True
    blink_timer = 0

    while True:
        screen.blit(bg_image, (0, 0))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 120))
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            opt_text = font.render(opt, True, color)
            y = 300 + i * 60
            if i == selected and blink:
                screen.blit(opt_text, (WINDOW_WIDTH // 2 - opt_text.get_width() // 2, y))
            elif i != selected:
                screen.blit(opt_text, (WINDOW_WIDTH // 2 - opt_text.get_width() // 2, y))
        pygame.display.flip()
        blink_timer += 1
        if blink_timer % 30 == 0:
            blink = not blink

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return  # Start Game
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()

# --- Game Over logic ---
def game_over_screen(final_score):
    options = ["Restart", "Quit"]
    selected = 0
    blink = True
    blink_timer = 0
    pygame.mixer.music.stop()
    while True:
        screen.blit(bg_image, (0, 0))
        over_text = big_font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        screen.blit(over_text, (WINDOW_WIDTH // 2 - over_text.get_width() // 2, 120))
        screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 220))
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            opt_text = font.render(opt, True, color)
            y = 350 + i * 60
            if i == selected and blink:
                screen.blit(opt_text, (WINDOW_WIDTH // 2 - opt_text.get_width() // 2, y))
            elif i != selected:
                screen.blit(opt_text, (WINDOW_WIDTH // 2 - opt_text.get_width() // 2, y))
        pygame.display.flip()
        blink_timer += 1
        if blink_timer % 30 == 0:
            blink = not blink

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return True  # Restart
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()

# --- Main game loop ---
def run_game():
    pygame.mixer.music.play(-1)

    player = Player(100, 100, os.path.join(SPRITES_DIR, "player.png"), WINDOW_WIDTH, WINDOW_HEIGHT)
    collectible = Collectible(WINDOW_WIDTH, WINDOW_HEIGHT, os.path.join(SPRITES_DIR, "collectible.png"))

    # plusieurs ennemis
    enemies = [
        Enemy(800, 100, os.path.join(SPRITES_DIR, "enemy.png"), 2, WINDOW_WIDTH, WINDOW_HEIGHT),
        Enemy(950, 300, os.path.join(SPRITES_DIR, "enemy.png"), 3, WINDOW_WIDTH, WINDOW_HEIGHT),
        Enemy(1100, 500, os.path.join(SPRITES_DIR, "enemy.png"), 4, WINDOW_WIDTH, WINDOW_HEIGHT)
    ]

    score = 0
    clock = pygame.time.Clock()
    game_over = False
    difficulty = 1.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)
        collectible.update()

        # difficulté augmente avec le score
        difficulty = 1.0 + score * 0.03

        # mise à jour ennemis
        for enemy in enemies:
            enemy.update(difficulty=difficulty, player_rect=player.rect)

        # collisions
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                collision_sound.play()
                pygame.mixer.music.stop()
                game_over = True
                break

        if player.rect.colliderect(collectible.rect) and collectible.active:
            collect_sound.play()
            score += 10
            collectible.collect()

        # dessin
        screen.blit(bg_image, (0, 0))
        player.draw(screen)
        collectible.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    restart = game_over_screen(score)
    if restart:
        run_game()

# --- Entry point ---
if __name__ == "__main__":
    main_menu()
    run_game()
