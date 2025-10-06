import pygame
import random
import math
import time

class Enemy:
    """
    Enemy avec mouvements complexes et comportement adaptatif.
    - Oscillation sinusoïdale
    - Dashes horizontaux aléatoires
    - Variation progressive de vitesse
    - Respawn contrôlé hors écran
    """
    def __init__(self, x, y, image_path, speed, window_width, window_height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.window_width = window_width
        self.window_height = window_height

        # paramètres de base
        self.base_speed = speed
        self.speed = float(speed)
        self.angle = 0.0
        self.amplitude = random.randint(30, 80)
        self.frequency = random.uniform(0.02, 0.05)
        self.vertical_dir = random.choice([-1, 1])
        self.last_dash_time = 0
        self.dash_cooldown = random.uniform(2, 4)  # secondes
        self.spawn_time = time.time()
        self.alive = True

    def update(self, difficulty=1.0, player_rect=None):
        """
        Met à jour la position de l'ennemi.
        - oscillation sinusoïdale
        - dash occasionnel vers le joueur
        - réapparition si l'ennemi quitte trop l'écran
        """
        if not self.alive:
            return

        # vitesse dynamique (augmente avec la difficulté)
        self.speed = self.base_speed + difficulty * 1.5

        # mouvement horizontal constant
        self.rect.x -= int(self.speed)

        # mouvement vertical sinusoïdal + bruit aléatoire
        self.angle += self.frequency
        self.rect.y += int(math.sin(self.angle) * self.amplitude * 0.05)
        self.rect.y += self.vertical_dir * random.randint(-1, 2)

        # dash vers le joueur (toutes les 2-4s)
        current_time = time.time()
        if player_rect and current_time - self.last_dash_time > self.dash_cooldown:
            if self.rect.centery < player_rect.centery:
                self.rect.y += random.randint(20, 40)
            elif self.rect.centery > player_rect.centery:
                self.rect.y -= random.randint(20, 40)
            self.last_dash_time = current_time
            self.dash_cooldown = random.uniform(1.5, 3.5)

        # rebond sur le haut/bas
        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.vertical_dir *= -1

        # disparition si hors écran trop longtemps
        if self.rect.right < -200:
            self.alive = False

        # respawn automatique
        if not self.alive:
            self.respawn()

    def respawn(self):
        """ Réapparaît à droite avec nouveaux paramètres """
        self.rect.x = self.window_width + random.randint(0, 150)
        self.rect.y = random.randint(0, self.window_height - self.rect.height)
        self.speed = self.base_speed + random.uniform(0, 2)
        self.amplitude = random.randint(30, 80)
        self.frequency = random.uniform(0.02, 0.05)
        self.vertical_dir = random.choice([-1, 1])
        self.last_dash_time = time.time()
        self.dash_cooldown = random.uniform(2, 4)
        self.alive = True

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
