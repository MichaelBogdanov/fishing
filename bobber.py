import pygame
from config import WIDTH, HEIGHT, FPS


class Bobber:
    def __init__(self, rod):
        self.rod = rod
        
        self.sprites = [
            pygame.transform.scale(pygame.image.load('images/bobber1.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('images/bobber2.png').convert_alpha(), (100, 100))
        ]
        self.scaled_sprites = self.sprites.copy()
        
        self.max_y = HEIGHT * 0.75 - HEIGHT / 3
        self.range = HEIGHT / 3
        self.distance = 100
        self.x = WIDTH / 2
        self.y = self.max_y
                
        self.speedup = 1
        self.size = 100 - self.distance * 0.5
        self.counter = 0
    
    def pull_up(self,):
        self.distance = max(0, self.distance - self.range / (self.range / self.rod.speed * 10))
        self.y = HEIGHT * 0.75 - HEIGHT / 3 / 100 * self.distance
    
    def update(self):
        # Подтягивает если закинули слишком далеко
        if abs(self.rod.x - (self.x + 50)) >= 300:
            self.x += self.rod.speed * (-1 + 2 * (self.rod.x > self.x))
        # Поплавок падает вниз
        if self.y < HEIGHT * 0.75 - HEIGHT / 3 / 100 * self.distance:
            self.speedup *= 1.05
            self.y += self.speedup
            self.y = min(self.y, HEIGHT * 0.75 - HEIGHT / 3 / 100 * self.distance)
        # Меняем размер в зависимости от дистанции
        self.size = 100 - self.distance * 0.5
        # Скалируем спрайты
        self.scaled_sprites = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)), self.sprites))
            
    def draw(self, screen):
        # Отрисовываем поплавок
        screen.blit(self.scaled_sprites[int(self.counter)], (self.x, self.y))
        
        # Отрисовываем леску
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (self.x + self.size * 0.5, self.y + self.size * 0.4 - self.size * 0.1 * int(self.counter)),
            (self.rod.x, self.rod.y),
            2
        )
        
        # Увеличиваем счётчик
        self.counter += 1 / FPS
        self.counter %= len(self.scaled_sprites)