import pygame
from config import WIDTH, HEIGHT, FPS


def draw_sagging_line(surf, rod_tip, float_pos):
    mid = ((rod_tip[0] + float_pos[0]) // 2,
           (rod_tip[1] + float_pos[1]) // 2 + 20)
    points = []
    for t in range(21):
        s = t / 20
        x = (1 - s)**2 * rod_tip[0] + 2 * (1 - s) * s * mid[0] + s**2 * float_pos[0]
        y = (1 - s)**2 * rod_tip[1] + 2 * (1 - s) * s * mid[1] + s**2 * float_pos[1]
        points.append((int(x), int(y)))
    if len(points) >= 2:
        pygame.draw.lines(surf, (255, 255, 255), False, points, 2)


class Bobber:
    def __init__(self, rod):
        self.rod = rod
        
        self.sprites = [
            pygame.transform.scale(pygame.image.load('images/bobber1.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('images/bobber2.png').convert_alpha(), (100, 100))
        ]
        self.scaled_sprites = self.sprites.copy()
        
        self.max_y = HEIGHT * 0.75 - HEIGHT / 2.5
        self.range = HEIGHT / 3
        self.x = WIDTH / 2
        self.y = 0
                
        self.speedup = 1
        self.size = 10
        self.counter = 0
        
        self.weight = 8 * 10 ** -3
    
    def update(self):
        # Скалируем спрайты
        self.scaled_sprites = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)), self.sprites))
            
    def draw(self, screen):
        # Отрисовываем поплавок
        screen.blit(self.scaled_sprites[int(self.counter)], (self.x, self.y))
        
        # Отрисовываем леску
        float_pos = (self.x + self.size * 0.5, self.y + self.size * 0.4 - self.size * 0.1 * int(self.counter))
        draw_sagging_line(screen, self.rod.attachment_point, float_pos)
        
        # Увеличиваем счётчик
        self.counter += 1 / FPS
        self.counter %= len(self.scaled_sprites)