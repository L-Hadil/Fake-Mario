import pygame

class Player:
    """
    Player class handles player movement and drawing.
    """
    def __init__(self, x, y, image_path, window_width, window_height):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.window_width = window_width
        self.window_height = window_height
        self.speed = 5

    def update(self, keys):
        # Move player with arrow keys, keep inside window boundaries
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Boundary checks
        self.rect.x = max(0, min(self.rect.x, self.window_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.window_height - self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)