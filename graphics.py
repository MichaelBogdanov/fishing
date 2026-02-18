import random
import pygame


# Функция для замены цвета в Surface
def replace_color(s: pygame.Surface, color1: tuple[int, int, int], color2: tuple[int, int, int]):
    """Закрашивает все пикселы поверхности s цвета color1 цветом color2."""
    for x in range(0, s.get_width()):
        for y in range(0, s.get_height()):
            if s.get_at((x, y)) == pygame.Color(color1):
                s.set_at((x, y), pygame.Color(color2))

# Эффект полос на экране
def scanlines(screen):
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))

    screen.blit(scanline_surface, (0, 0))

# Эффект пикселизации экрана
def pixelation(screen, pixelation=2):
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // pixelation, height // pixelation))
    screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))

# Эффект глитча экрана
def glitch(height, width, glitch_surface, intensity):
    shift_amount = {"minimum": 10, "medium": 20, "maximum": 40}.get(intensity, 20)
    if random.random() < 0.1:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pygame.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))

# Вспомогательные линии для физики
def physics_interface(screen):
    pygame.draw.line(screen, (255, 255, 255), (screen.get_width() // 2, screen.get_height()), (0, 0), 5)
    pygame.draw.line(screen, (255, 255, 255), (screen.get_width() // 2, screen.get_height()), (screen.get_width(), 0), 5)