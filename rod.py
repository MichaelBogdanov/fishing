import pygame

from config import WIDTH, HEIGHT


class Rod:
    def __init__(self):
        self.sprites = [
            pygame.transform.scale(pygame.image.load('images/rod1.png').convert_alpha(), (WIDTH / 4, HEIGHT / 3)),
            pygame.transform.scale(pygame.image.load('images/rod2.png').convert_alpha(), (WIDTH / 4, HEIGHT / 3)),
            pygame.transform.scale(pygame.image.load('images/rod3.png').convert_alpha(), (WIDTH / 4, HEIGHT / 3))
        ]
        self.x = WIDTH // 2
        self.y = HEIGHT - max(map(lambda x: x.get_height(), self.sprites)) - 50
        self.speed = 20
        
        self.length = 1.5
    
    def draw(self, surface):
        if self.x <= WIDTH / 3:
            surface.blit(self.sprites[2], (self.x, self.y))
        elif self.x <= WIDTH / 3 * 2:
            surface.blit(self.sprites[1], (self.x - self.sprites[1].get_width() / 2, self.y))
        else:
            surface.blit(self.sprites[0], (self.x - self.sprites[0].get_width(), self.y))