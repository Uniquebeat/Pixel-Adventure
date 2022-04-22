import pygame, sys, time
from setting import *
from level import Level
from debug import debug


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((scaled_width, scaled_height), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption('Pixel_Adventure_1')
        self.clock = pygame.time.Clock()
        self.prev_time = time.time()
        self.level = Level()

    def run(self):
        while True:
            dt = time.time() - self.prev_time
            self.prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       pygame.quit()
                       sys.exit()

            self.screen.fill((33, 31, 48))
            self.level.run(dt)
            debug('FPS', int(self.clock.get_fps()), 40)

            pygame.display.update()
            self.clock.tick(fps)


if __name__ == '__main__':
    game = Game()
    game.run()
