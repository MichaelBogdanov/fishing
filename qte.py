import sys
import math
import random
import pygame


class Minigame:
    def __init__(self, screen, bar, difficult=0):
        self.screen = screen
        self.bar = bar

        self.width = 400
        self.height = 50
        self.rect_x = screen.get_width() // 2 - self.width // 2
        self.rect_y = 50
        self.rect = pygame.Rect(self.rect_x, self.rect_y, self.width, self.height)

        self.crosshair_x = float(self.rect_x)
        self.crosshair_w = 3
        self.crosshair_dir = 1

        self.score = 0

        # --- МОДЕЛЬ СЛОЖНОСТИ (основана на реакции человека) ---
        self.v0 = 300.00 + difficult * 50.00
        self.v_max = 600.00 + difficult * 50.00
        self.k_v = 0.30 + difficult * 0.05

        self.T0 = 0.30 - difficult * 0.03
        self.T_min = 0.03 - difficult * 0.002
        self.k_t = 0.30 + difficult * 0.05

        self.target_min_w = 1

        self.target = self.new_target()

    def current_speed(self):
        return self.v0 + (self.v_max - self.v0) * (1 - math.exp(-self.k_v * self.score))

    def current_window(self):
        return self.T_min + (self.T0 - self.T_min) * math.exp(-self.k_t * self.score)

    def new_target(self):
        v = self.current_speed()
        T = self.current_window()

        w = max(self.target_min_w, int(v * T))
        w = min(w, self.width)

        x = random.randint(self.rect_x, self.rect_x + self.width - w)
        return pygame.Rect(x, self.rect_y, w, self.height)

    def click(self):
        crosshair_rect = pygame.Rect(int(self.crosshair_x), self.rect_y, self.crosshair_w, self.height)
        if self.target.colliderect(crosshair_rect):
            self.score += 1
            self.target = self.new_target()
            self.crosshair_x = float(self.rect_x)
            self.crosshair_dir = 1
            self.bar.success()
            return True
        self.bar.success(0)
        return False

    def update(self, dt):
        speed = self.current_speed()
        self.crosshair_x += self.crosshair_dir * speed * dt

        left = self.rect_x
        right = self.rect_x + self.width - self.crosshair_w

        if self.crosshair_x >= right:
            self.crosshair_x = right
            self.crosshair_dir = -1
        elif self.crosshair_x <= left:
            self.crosshair_x = left
            self.crosshair_dir = 1

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

        pygame.draw.rect(self.screen, (60, 180, 75), self.target)
        pygame.draw.rect(self.screen, (50, 50, 50),
                         (int(self.crosshair_x), self.rect_y, self.crosshair_w, self.height))

        if __name__ == "__main__":
            speed = self.current_speed()
            window = self.current_window()
            font = pygame.font.SysFont("Сonsolas", 36)

            texts = [
                f"Счёт: {self.score}",
                f"Скорость: {speed:.1f}px/s",
                f"Окно попадания: {int(window * 1000)} мс",
                "Нажмите ЛКМ, когда красная линия находится внутри зеленой зоны"
            ]

            for i, t in enumerate(texts):
                surf = font.render(t, True, (230, 230, 230))
                self.screen.blit(surf, (screen.get_width() // 2 - surf.get_width() // 2, screen.get_height() // 2 - surf.get_height() // 2 + i * 36))

class MinigameBar:
    def __init__(self, screen, difficult=0):
        self.screen = screen
        self.difficult = difficult
        
        self.width = 50
        self.height = 400
    
        self.rect_y = screen.get_height() // 2 - self.height // 2
        self.rect_x = 50
        self.rect = pygame.Rect(self.rect_x, self.rect_y, self.width, self.height)
        
        self.value_percent = 30

    def success(self, value=30):
        self.value_percent += value - self.difficult

    def update(self, dt):
        self.value_percent -= 10 * dt
        if self.value_percent < 0:
            self.value_percent = 0
            return False
        elif self.value_percent > 100:
            self.value_percent = 100
            return True
        self.value_height = self.value_percent * self.height / 100
        self.value = pygame.Rect(self.rect_x, self.rect_y + self.height - self.value_height, self.width, self.value_height + 1)
        return None

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        pygame.draw.rect(self.screen, (60, 180, 75), self.value)


def main():
    global accumulator
    bar = MinigameBar(screen, difficult=5)
    game = Minigame(screen, bar, difficult=5)

    while True:
        frame_dt = clock.tick(FPS) / 1000
        frame_dt = min(frame_dt, 0.05)
        accumulator += frame_dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game.click():
                        print("Попадание!", game.score)

        while accumulator >= LOGIC_DT:
            game.update(LOGIC_DT)
            accumulator -= LOGIC_DT
            result = bar.update(LOGIC_DT)
            if result is True:
                print("Вы выиграли!")
                pygame.quit()
                sys.exit()
            elif result is False:
                print("Вы проиграли!")
                pygame.quit()
                sys.exit()

        screen.fill((10, 10, 10))
        game.draw()
        bar.draw()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    SCREEN_W, SCREEN_H = 1920, 1080
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Игра на реакцию")

    clock = pygame.time.Clock()
    FPS = 60

    LOGIC_FPS = 240
    LOGIC_DT = 1 / LOGIC_FPS
    accumulator = 0.0
    
    main()
