import pygame
import random
import time

class Collectible:
    """
    Represents a collectible item that the player can pick up.
    Spawns at random positions, disappears when collected, and respawns after a delay.
    """
    def __init__(self, window_width, window_height, image_path, respawn_delay=2):
        self.window_width = window_width
        self.window_height = window_height
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.respawn_delay = respawn_delay  # seconds
        self.active = True
        self.last_collected_time = None
        self.spawn()

    def spawn(self):
        # Place at a random position within window boundaries
        self.rect.x = random.randint(0, self.window_width - self.rect.width)
        self.rect.y = random.randint(0, self.window_height - self.rect.height)
        self.active = True

    def collect(self):
        # Called when player collects the item
        self.active = False
        self.last_collected_time = time.time()

    def update(self):
        # Handle respawn logic
        if not self.active and self.last_collected_time:
            if time.time() - self.last_collected_time >= self.respawn_delay:
                self.spawn()

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect)
