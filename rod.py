import math

import pygame

from config import WIDTH, HEIGHT


class Rod:
    def __init__(self, path, speed, length):
        self.original_sprite = pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            (60, 300)
        )

        self.sprite = self.original_sprite
        self.rect = self.sprite.get_rect()
        self.rect.centerx = WIDTH / 2

        self.angle = 0
        self.speed = speed
        
        self.length = length

    def update(self, yaw):
        new_x = self.rect.centerx + self.speed * yaw / (WIDTH / 2)
        new_x = max(WIDTH / 2 - 200, min(WIDTH / 2 + 200, new_x))

        if new_x != self.rect.centerx:
            self.angle = -450 * new_x / WIDTH + 225
            
            self.sprite = pygame.transform.rotate(self.original_sprite, self.angle)
            self.rect = self.sprite.get_rect()

            self.rect.centerx = new_x
            self.diff_y = abs(-100 * math.sin(math.radians(self.angle)))
            self.rect.centery = HEIGHT - self.rect.height / 2 - 100 + self.diff_y

    def draw(self, surface):
        surface.blit(self.sprite, self.rect)
