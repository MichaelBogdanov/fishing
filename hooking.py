import sys
import time
import pygame
from math import ceil
from random import randint

from config import WIDTH, HEIGHT, SCREEN, FPS, MYFONT
from messages import send_message
from rod import Rod


HOOKING_RADIUS = HEIGHT // 10 // 2


def color_generator(step):
    for i in range(0, 256, int(step)):
        yield (i, 255, 0)
    for i in range(1, 256, int(step)):
        yield (255, int(255 - i), 0)


class Hooking:
    def __init__(self, rod):
        self.radius = HOOKING_RADIUS
        self.x = randint(self.radius, WIDTH - self.radius)
        self.y = randint(self.radius, HEIGHT - self.radius)
        
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        self.sight_step = ((255 * 2.5) * (1 - 0.2 * rod.quality)) / HOOKING_RADIUS
        self.sight_radius = 0
        self.sight_color = iter(color_generator(self.sight_step))
        
        self.rod = rod
    
    def click(self):
        return 100 - int(self.sight_radius / self.radius * 100)
    
    def update(self):
        self.sight_radius += 1 - 0.25 * self.rod.quality
        if self.sight_radius >= self.radius:
            return False
        
    def draw(self):
        pygame.draw.circle(self.surface, (255, 255, 255, 128), (self.radius, self.radius), self.radius)
        SCREEN.blit(self.surface, (self.x - self.radius, self.y - self.radius))
        try:
            color = next(self.sight_color)
        except:
            color = (255, 0, 0)
        pygame.draw.circle(SCREEN, color, (self.x, self.y), self.sight_radius, 5)


if __name__ == "__main__":
    pygame.display.set_caption("Подсечка рыбы")
    
    clock = pygame.time.Clock()
    
    rod = Rod('images/rod.png', 20, 1.5, 3)
    hooking = Hooking(rod)
    message = None
    delay = FPS
    
    while True:
        clock.tick(FPS)
        
        SCREEN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not delay:
                    message = send_message(str(hooking.click()), MYFONT, (255, 255, 255))
                    hooking = Hooking(rod)
                    delay = FPS + randint(0, FPS)
        
        if not delay:
            if result := hooking.update() == False:
                hooking = Hooking(rod)
                delay = FPS + randint(0, FPS)
            else:
                hooking.draw()
        
        try:
            message_frame = next(message)
            SCREEN.blit(message_frame, (SCREEN.width // 2 - message_frame.get_width() // 2, SCREEN.height * 0.8))
        except:
            pass
        
        if delay > 0:
            delay -= 1
        
        pygame.display.flip()