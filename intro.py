import sys
import pygame

from config import WIDTH, HEIGHT, SCREEN, FPS, MYFONT
from messages import send_message
from graphics import pixelation


story = [
    "Эта история произошла давно.",
    "Устав от серой обыденности,",
    "монотонной рабочей рутины,",
    "дней, ничем не отличающихся друг от друга,",
    "решив сбросить оковы системы",
    "и начать жизнь с чистого листа,",
    "я отправился в путешествие по морю,",
    "устроившись матросом на торговое судно.",
    "Я хотел посмотреть мир,",
    "вновь почувствовать вкус жизни...",
    "..."
]


def prolog():
    clock = pygame.time.Clock()
    
    pygame.display.set_caption("Пролог")
    
    story_index = 0
    story_frames = iter(send_message(story[story_index], MYFONT))
    
    storm = pygame.image.load('images/storm.jpg')
    storm = pygame.transform.scale(storm, (WIDTH, HEIGHT))
    pixelation(storm, 3)
    
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        try:
            if story_index >= 10:
                SCREEN.blit(storm, (0, 0))
            else:
                SCREEN.fill((0, 0, 0))
            story_frame = next(story_frames)
            SCREEN.blit(story_frame, (SCREEN.width // 2 - story_frame.get_width() // 2, SCREEN.height * 0.8))
        except:
            story_index += 1
            try:
                story_frames = iter(send_message(story[story_index], MYFONT))
            except:
                return

        pygame.display.flip()


if __name__ == "__main__":
    prolog()
