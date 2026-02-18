import os
import pygame

from config import WIDTH, HEIGHT, SCREEN

# Уровни
class Level:
    def __init__(self, number: int, name: str, pos: list[int], quota: int, background_path: str, open: bool = False, pier_path: str = 'images/pier.png'):
        self.number = number
        self.name = name
        self.pos = pos
        self.quota = quota
        self.part_of_raft = False
        self.sprites_path = background_path
        self.open = open

        # Подготовим фон один раз (precompose). Используем Surface с альфой на всякий случай.
        self.background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
        # Загружаем все изображения слоями и сразу блим их на background.
        # Сортируем список, чтобы порядок был детерминирован (если нужно — поменяйте по вашему).
        try:
            filenames = sorted(os.listdir(background_path))
        except FileNotFoundError:
            filenames = []

        for filename in filenames:
            # Пропускаем не-графику (например .DS_Store и т.п.)
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                continue
            full = os.path.join(self.sprites_path, filename)
            try:
                sprite = pygame.image.load(full)
            except Exception:
                continue
            # Сохраняем альфу, если она есть
            if sprite.get_alpha() is not None:
                sprite = sprite.convert_alpha()
            else:
                sprite = sprite.convert()
            # Масштабируем один раз к размеру экрана
            if sprite.get_size() != (WIDTH, HEIGHT):
                sprite = pygame.transform.scale(sprite, (WIDTH, HEIGHT))
            # Блим на фон
            self.background.blit(sprite, (0, 0))
        
        pier = pygame.image.load(pier_path)
        # Сохраняем альфу, если она есть
        if pier.get_alpha() is not None:
            pier = pier.convert_alpha()
        else:
            pier = pier.convert()
        # Масштабируем один раз к размеру экрана
        pier = pygame.transform.scale(pier, (WIDTH * (pier.get_width() / 480), HEIGHT * (pier.get_height() / 180)))
        # Блим на фон
        pier_rect = pier.get_rect()
        pier_rect.centerx = WIDTH // 2
        pier_rect.y = HEIGHT - pier.get_height()
        self.background.blit(pier, (pier_rect.x, pier_rect.y))

    def update(self):
        ...

    def draw(self):
        # Один blit вместо множества
        SCREEN.blit(self.background, (0, 0))


levels = [
    # Уровень 1 - Лес
    Level(1, 'Лес', [690, 345], 20_000, 'images/level1/', True),
    # Уровень 2 - Болотистая местность
    Level(2, 'Болото', [1230, 150], 50_000, 'images/level1/'),
    # Уровень 3 - Пустыня
    Level(3, 'Пустыня', [1610, 250], 100_000, 'images/level1/'),
    # Уровень 4 - Саванна
    Level(4, 'Саванна', [1470, 450], 150_000, 'images/level1/'),
    # Уровень 5 - Вулкан
    Level(5, 'Вулкан', [1075, 650], 250_000, 'images/level1/'),
    # Уровень 6 - Озеро во льдах
    Level(6, 'Озеро во льдах', [125, 715], 500_000, 'images/level1/'),
]

current_level = None
