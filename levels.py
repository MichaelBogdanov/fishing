from dataclasses import dataclass
import gif_pygame


# Уровни
@dataclass
class Level:
    number: int
    name: str
    pos: list[int]
    quota: int
    open: bool
    part_of_raft: bool
    background: gif_pygame.GIFPygame

levels = [
    # Уровень 1 - Лес
    Level(1, 'Лес', [690, 345], 20_000, True, False, gif_pygame.load('images/bg.gif')),
    # Уровень 2 - Болотистая местность
    Level(2, 'Болото', [1230, 150], 50_000, False, False, gif_pygame.load('images/bg.gif')),
    # Уровень 3 - Пустыня
    Level(3, 'Пустыня', [1610, 250], 150_000, False, False, gif_pygame.load('images/bg.gif')),
    # Уровень 4 - Саванна
    Level(4, 'Саванна', [1470, 450], 100_000, False, False, gif_pygame.load('images/bg.gif')),
    # Уровень 5 - Вулкан
    Level(5, 'Вулкан', [1075, 650], 250_000, False, False, gif_pygame.load('images/bg.gif')),
    # Уровень 6 - Озеро во льдах
    Level(6, 'Озеро во льдах', [125, 715], 500_000, False, False, gif_pygame.load('images/bg.gif')),
]

current_level = None