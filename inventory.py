import pygame

from config import SCREEN, WIDTH, HEIGHT


class Inventory:
    def __init__(self):
        self.width = WIDTH / 2
        self.height = HEIGHT / 6
        self.surface = pygame.Surface((self.width, self.height)).convert_alpha()
        self.shift_x = 0
        self.shift_y = -self.height
        self.item_width = self.height
        self.rect = pygame.Rect((WIDTH / 4, self.shift_y, self.width, self.height))
        self.speed = 10
        self.items = []
        self.inventory_length = 0
        self.taken = None
    
    def add_item(self, item):
        if item not in self.items:
            self.items.append((item, 1))
        else:
            for i, (inv_item, count) in enumerate(self.items):
                if inv_item == item:
                    self.items[i] = (inv_item, count + 1)
                    break
        
    def update(self, mouse_pos):
        # Открытие
        if mouse_pos[1] <= self.height:
            self.shift_y = min(0, self.shift_y + self.speed)
        else:
            self.shift_y = max(-self.height, self.shift_y - self.speed)
        self.rect.top = self.shift_y
        
        # Отрисовка
        self.surface.fill((100, 100, 0, 128))
        
        # Добавление предметов
        for i, item in enumerate(self.items):
            image = pygame.transform.scale(item[0].image, (self.item_width, self.item_width))
            rect = pygame.Rect(self.shift_x + self.item_width * i, 0, self.item_width, self.item_width)
            
            # Отрисовка прдметов
            if not item[0] is self.taken:
                self.surface.blit(image, rect)
            
            # Взятие предметов
            rect.left = WIDTH / 4 + self.shift_x + self.item_width * i
            rect.top = self.shift_y
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos) and self.taken is None:
                self.taken = item[0]
        
        # Отрисовка взятого предмета
        if self.taken is not None:
            # Отпускание предметов
            if not pygame.mouse.get_pressed()[0]:
                self.taken = None
            else:
                preview_image = pygame.transform.scale(self.taken.image, (self.height, self.height))
                SCREEN.blit(preview_image, mouse_pos)
        
        # Обновление длины инвентаря
        self.inventory_length = len(self.items) * self.item_width
        
    def draw(self):
        SCREEN.blit(self.surface, self.rect)