import sys
import pygame
from dataclasses import dataclass
from server import get_fish_rarities_from_server


# Рыбы
@dataclass
class Fish:
    rarity: float
    name: str
    image: pygame.Surface


# Загрузка редкостей рыб
try:
    fish_rarity = get_fish_rarities_from_server()
    print("Загружены редкости рыб с сервера")
except:
    print("Не удалось загрузить редкости рыб с сервера...")
    sys.exit()

# Список рыб
fish = [
    [
        Fish(fish_rarity[0], 'Обычный окунь', pygame.image.load('images/fish/0large_mouth_bass.png').convert_alpha()),
        Fish(fish_rarity[0], 'Каменный окунь', pygame.image.load('images/fish/0rock_bass.png').convert_alpha())
    ],
    [
        Fish(fish_rarity[1], 'Синежаберник', pygame.image.load('images/fish/1bluegill_panfish.png').convert_alpha()),
        Fish(fish_rarity[1], 'Пятнистый окунь', pygame.image.load('images/fish/1spotted_bass.png').convert_alpha()),
        Fish(fish_rarity[1], 'Краппи', pygame.image.load('images/fish/1black_crappie.png').convert_alpha())
    ],
    [
        Fish(fish_rarity[2], 'Чёрный окунь', pygame.image.load('images/fish/2black_bass.png').convert_alpha()),
        Fish(fish_rarity[2], 'Красногрудный солнечник', pygame.image.load('images/fish/2redbreast_sunfish_panfish.png').convert_alpha())
    ],
    [
        Fish(fish_rarity[3], 'Судак', pygame.image.load('images/fish/3walleye.png').convert_alpha()),
        Fish(fish_rarity[3], 'Жёлтый судак', pygame.image.load('images/fish/3yellow_perch.png').convert_alpha())
    ],
    [
        Fish(fish_rarity[4], 'Сом', pygame.image.load('images/fish/4channel_catfish.png').convert_alpha()),
        Fish(fish_rarity[4], 'Плоскоголовый сом', pygame.image.load('images/fish/4flathead_catfish.png').convert_alpha())
    ], 
    [
        Fish(fish_rarity[5], 'Щука', pygame.image.load('images/fish/5muskie.png').convert_alpha())
    ]       
]
    