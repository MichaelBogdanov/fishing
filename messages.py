import sys
import pygame


def send_message(text: str, font: pygame.font.Font, color: list[int] = (255, 255, 255), frames: int = 180):
    for i in range(1, len(text) + 1):
        frames -= 1
        label = font.render(text[:i], 1, color)
        yield label
    for _ in range(frames):
        yield label


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    FPS = 60
    
    pygame.font.init()
    font = pygame.font.Font("Comic Sans MS Pixel.ttf", 64)

    message_frames = iter(send_message("Приветствую, игрок! Выйти из игры на ESC!", font))

    while True:
        clock.tick(FPS)
        
        screen.fill((0, 0, 0))
        try:
            message_frame = next(message_frames)
            screen.blit(message_frame, (screen.width // 2 - message_frame.get_width() // 2, screen.height * 0.8))
        except:
            pass
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()