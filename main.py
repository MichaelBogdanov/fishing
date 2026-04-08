import os
import sys
import math
import random

import pygame
import gif_pygame
from dotenv import load_dotenv

# Меняем рабочую директорию на папку с файлом
os.chdir(os.path.dirname(__file__))
# Загрузка переменных окружения из .env файла
load_dotenv('.env')

from config import SCREEN, WIDTH, HEIGHT, FPS, MINIGAME_DT, MYFONT
from server import auth_menu, update_server_score
from messages import send_message
from inventory import Inventory
from hooking import Hooking
from qte import Minigame, MinigameBar
from graphics import *


# Основная функция игры
def main(user_data):
    # Инициализация pygame
    pygame.init()
    # Инициализация микшера для звуков
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)

    # Загрузка параметров игры
    accumulator = 0.0
    clock = pygame.time.Clock()
    fps_counter = 0
    
    # Изменяем подпись у окна
    pygame.display.set_caption('Рыбалка на Pygame')
    
    # Создание карты игры
    game_map = gif_pygame.load('images/map.gif')
    gif_pygame.transform.scale(game_map, (WIDTH, HEIGHT))
    
    # Загрузка уровней
    from levels import levels, current_level
    
    # Загрузка рыб
    from fish import fish, fish_rarity
    
    # Загрузка музыки
    from music import levels_music, playlist
    song = random.choice(levels_music[current_level])
    pygame.mixer.music.load('sound/' + song)
    pygame.mixer.music.play()
    playlist.append(song)
    
    # Загрузка данных пользователя
    score = user_data['score']
    
    # Закидывание
    throwing_status = False
    # Рыбалка
    fishing_status = False
    # Подсечка
    hooking_status = False
    hooking = Hooking()
    # Ловля
    catch_status = False
    # Анимация ловли
    catch_animation_status = False
    
    # Удочка
    from rod import Rod
    rod = Rod('images/rod.png', 20, 1.5)
    
    # Поплавок
    from bobber import Bobber
    bobber = Bobber(rod)

    # Интерфейс
    # Приманка
    bait = pygame.image.load('images/worm.png').convert_alpha()
    bait = pygame.transform.scale(bait, (64, 64))
    bait_count = 5
    bait_now = bait_count
    bait_positions = [WIDTH - x - 64 for x in range(64, 64 * bait_count + 1, 64)]
    # Очки
    pygame.font.init()
    score_label = MYFONT.render(f"Score: {score}", 1, (255, 255, 255))
    # Инвентарь
    inventory = Inventory()
    for elem in [*fish[0], *fish[1], *fish[2]]:
        inventory.add_item(elem)

    try:
        # Игровой цикл
        while True:
            # Ограничиваем FPS и создаём дельту времени для мини-игр
            frame_dt = clock.tick(FPS) / 1000
            frame_dt = min(frame_dt, 0.05)
            accumulator += frame_dt
            fps_counter += 1
            
            # Собираем события за кадр
            events = pygame.event.get()
            
            # Возможность выхода из игры
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not current_level):
                    # Закрытие игры
                    update_server_score(user_data['username'], score)
                    pygame.quit()
                    sys.exit()
            
            # Проверяем на уровне ли мы? Или на карте?
            if current_level != None:
                # Закрашиваем экран
                current_level.draw()
                
                # Обработка игровых событий
                for event in events:
                    match event.type:
                        # Нажатие клавиш на клавиатуре
                        case pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                current_level = None
                        # Нажатие клавиш мыши
                        case pygame.MOUSEBUTTONDOWN:
                            # Если нажали ЛКМ
                            if event.button == 1:
                                # Подсечка рыбы
                                if hooking_status:
                                    _ = hooking.click()
                                    hooking_status = False
                                    # Начинаем мини-игру
                                    catch_status = True
                                    # Создаём игру
                                    difficult = fish_rarity[::-1].index(now_rarity)
                                    fishing_bar = MinigameBar(SCREEN, difficult)
                                    game = Minigame(SCREEN, fishing_bar, difficult)
                                # Мини-игра
                                if catch_status:
                                    # Промах в мини-игре
                                    if not catch_animation_status:
                                        bait_now -= not game.click()
                                    # Сброс анимации
                                    else:
                                        catch_animation_percent = 120.00
                        # Прокрутка меню
                        case pygame.MOUSEWHEEL:
                            if event.y > 0:
                                inventory.shift_x = min(inventory.shift_x + inventory.speed * 3, 0)
                            elif event.y < 0:
                                inventory.shift_x = max(inventory.shift_x - inventory.speed * 3, -inventory.inventory_length + inventory.width)

                # Обработка мышки
                if not catch_status:
                    pressed_buttons = pygame.mouse.get_pressed()
                # Управление удочкой с помощью мышки
                if pressed_buttons[0] and not hooking_status:
                    # Двигаем удочку
                    mouse_x = pygame.mouse.get_pos()[0]
                    # Вычисляем отклонение позиции мышки от центра экрана по X
                    yaw = mouse_x - WIDTH / 2
                    # Задаём скорость движения в зависимости от отклонение
                    rod.update(yaw)

                # Если удочку забросили и ловят рыбу
                if fishing_status:
                    # Отрисовываем поплавок
                    bobber.update()
                    bobber.draw(SCREEN)
                    
                    # Шанс поклёвки
                    if fps_counter % FPS == 0:
                        # Если рыба клюёт
                        if random.randint(1, 100) <= 10 and not catch_status:
                            # Выбираем редкость рыбы
                            number = random.randint(1, 100_000) / 1_000
                            chance = 0
                            for rarity in fish_rarity:
                                chance += rarity['chance']
                                if number <= chance:
                                    print(f'Выпало: {number} - рыба {rarity["name"]}')
                                    now_rarity = rarity
                                    break
                            # Подсекаем
                            hooking_status = True
                            hooking = Hooking()
                            message = send_message('Жми ЛКМ: клюёт', MYFONT)

                # Отрисовываем удочку
                rod.draw(SCREEN)
                
                # Отрисовка интерфейса
                # Рисуем приманку
                for i in range(bait_now):
                    SCREEN.blit(bait, (bait_positions[i], 50))
                # Рисуем очки
                SCREEN.blit(score_label, (50, 52))
                
                # Рисуем инвентарь
                inventory.draw()
                inventory.update(pygame.mouse.get_pos(), current_level)
                
                # Забрасывание удочки
                if pressed_buttons[2] and not hooking_status:
                    if not throwing_status:
                        throwing_status = True
                        percent = 0
                        throwing_speed = 1
                    else:
                        if percent >= 100:
                            direction = 'Вниз'
                        elif percent <= 0:
                            direction = 'Вверх'
                        throwing_speed += 0.1 if direction == 'Вверх' else -0.1
                        percent += throwing_speed if direction == 'Вверх' else -throwing_speed
                        percent = max(0, percent)
                        percent = min(100, percent)
                    bar_height = 400
                    x, y = 50, SCREEN.get_height() // 2 - bar_height // 2
                    progress_height = bar_height / 100 * percent
                    pygame.draw.rect(SCREEN, (255, 255, 255), (x, y, 50, bar_height))
                    pygame.draw.rect(SCREEN, (60, 180, 75), (x, y + bar_height - progress_height + 1, 50, progress_height))
                # Бросок
                elif throwing_status:
                    throwing_status = False
                    
                    x0 = WIDTH / 2
                    y0 = HEIGHT - 150
                    a = WIDTH / (2 * (2 - percent / 100))
                    b = HEIGHT / (3 * (2 - percent / 100))
                    bobber.x = x0 + a * math.cos(math.radians(rod.angle + 90))
                    bobber.y = y0 + b * math.sin(math.radians(rod.angle - 90))
                    bobber.size = 30 - 15 * (percent / 100) + 10 * (abs(rod.angle) / 45)
                    
                    fps_counter = 0
                    fishing_status = True
                
                # Мини-игра
                if catch_status:
                    # Проверяем результат
                    if not catch_animation_status:
                        while accumulator >= MINIGAME_DT:
                            game.update(MINIGAME_DT)
                            accumulator -= MINIGAME_DT
                        game.draw()
                        result = fishing_bar.update(MINIGAME_DT)
                    # Рыбу поймали
                    if result == True and not catch_animation_status:
                        catch_animation_status = True
                        catch_animation_percent = 0.00
                        # Выбор рыбы
                        index = fish_rarity[::-1].index(now_rarity)
                        catch_fish = random.choice(fish[index])
                        message = send_message(catch_fish.name, MYFONT, now_rarity['color'], 120)
                    # Анимация ловли
                    if catch_animation_status:
                        catch_animation_percent += 1
                        if catch_animation_percent <= 30:
                            catch_fish_size = [
                                catch_fish.image.width * catch_animation_percent,
                                catch_fish.image.height * catch_animation_percent
                            ]
                            image = pygame.transform.scale(catch_fish.image, catch_fish_size)
                            image_rect = image.get_rect()
                            image_rect.center = (WIDTH // 2, HEIGHT // 2)
                        SCREEN.blit(image, image_rect)
                        # Конец анимации
                        if catch_animation_percent >= 120.00:
                            # Добавляем рыбу в инвентарь
                            inventory.add_item(catch_fish)
                            # Обновляем состояния
                            del fishing_bar
                            del game
                            catch_status = False
                            fishing_status = False
                            throwing_status = False
                            # Добавляем очки за рыбу
                            score += now_rarity['score']
                            score_label = MYFONT.render(f"Score: {score}", 1, now_rarity['color'])
                            # Обновляем счет на сервере при изменении
                            user_data['score'] = score
                            update_server_score(user_data['username'], score)
                            catch_animation_status = False
                    if result == False:
                        # Рыба сорвалась
                        catch_status = False
                        fishing_status = False
                        throwing_status = False
                    if not catch_animation_status and catch_status:
                        fishing_bar.draw()
            else:
                # Мы на карте
                game_map.render(SCREEN, (0, 0))
                
                # Открытие новых уровней
                for i in range(len(levels)):
                    # Открываем следующий, если выполнили квоту этого
                    if score >= levels[i].quota:
                        # Проверяем что уровень не последний
                        if i + 1 != len(levels):
                            levels[i + 1].open = True
                        # Появляется возможность выловить запчасть плота
                        levels[i].part_of_raft = True
                    # Рисуем кружочек с уровнем
                    color = (255, 255, 255) if levels[i].open else (150, 150, 150)
                    levels[i].point = pygame.draw.circle(SCREEN, color, levels[i].pos, 20, 0)
                
                # Обработка кликов на метки уровней
                for event in events:
                    match event.type:
                        # Клик мышкой
                        case pygame.MOUSEBUTTONDOWN:
                            for level in levels:
                                if level.open:
                                    if level.point.collidepoint(pygame.mouse.get_pos()):
                                        current_level = level
            
            # Подсекание рыбы
            if hooking_status:
                # Не успели подсечь
                if result := hooking.update() == False:
                    # Сорвалась
                    hooking_status = False
                    hooking = Hooking()
                else:
                    hooking.draw()
            
            # Вывод сообщений
            try:
                message_frame = next(message)
                SCREEN.blit(message_frame, (SCREEN.width // 2 - message_frame.get_width() // 2, SCREEN.height * 0.8))
            except:
                pass

            # Обновление экрана
            # pixelation(SCREEN, 3)
            # physics_interface(SCREEN)
            scanlines(SCREEN)
            glitch(SCREEN.get_height(), SCREEN.get_width(), SCREEN, "medium")
            pygame.display.flip()
            
            # Проверка звуков
            if not pygame.mixer.music.get_busy() or \
                playlist[-1] not in levels_music[current_level.number if current_level else None]:
                # Запускаем новую композицию
                song = random.choice(levels_music[current_level.number if current_level else None])
                pygame.mixer.music.load('sound/' + song)
                pygame.mixer.music.play()
                playlist.append(song)
    except KeyboardInterrupt:
        # Сохраняем счет при выходе
        update_server_score(user_data['username'], score)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Проверяем первый ли раз запускают игру
    if not os.getenv('PROLOG'):
        from intro import prolog
        prolog()
    
    # Запуск меню авторизации
    if (login := os.getenv('LOGIN')) and (password := os.getenv('PASSWORD')):
        user_data = auth_menu("1", login, password)
    else:
        user_data = auth_menu()
    if user_data:
        # Запуск основной игры
        main(user_data)
    else:
        print("Не удалось войти в систему")
