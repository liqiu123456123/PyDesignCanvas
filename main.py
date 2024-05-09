# -*- coding: utf-8 -*-
import math
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import random
class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 1
        self.drawing = False
        self.last_pos = None
        self.space = 1
        self.brush = pygame.image.load("img/画笔.png").convert_alpha()
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))

    # 开始绘画
    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def get_current_brush(self):
        return self.brush_now

    def set_size(self, size):
        if size < 0.5:
            size = 0.5
        elif size > 32:
            size = 32
        self.size = size
        self.brush_now = self.brush.subsurface((0, 0), (size * 2, size * 2))

    def get_size(self):
        return self.size

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                pygame.draw.circle(self.screen, self.color, p, int(self.size))
            self.last_pos = pos

    def _get_points(self, pos):
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x ** 2 + len_y ** 2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append(
                (points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        self.generate_random_colors()
        self.eraser_color = (0xff, 0xff, 0xff)
        self.colors_rect = []
        x_start = 364
        y_start = 10
        width = 32
        height = 32
        spacing = 2
        cols = 12

        for i in range(len(self.colors)):
            x = x_start + (i % cols) * (width + spacing)
            y = y_start + (i // cols) * (height + spacing)
            rect = pygame.Rect(x, y, width, height)
            self.colors_rect.append(rect)
        self.pens = [
            pygame.image.load("img/画笔.png").convert_alpha(),
        ]
        self.erasers = [
            pygame.image.load("img/橡皮擦.png").convert_alpha(),
        ]
        self.save_img = [
            pygame.image.load("img/保存.png").convert_alpha(),
        ]

        self.erasers_rect = []
        for (i, img) in enumerate(self.erasers):
            rect_x = 10 + (i + 1) * 64
            rect_y = 10
            rect = pygame.Rect(rect_x+30, rect_y + i * 64, 64, 64)
            self.erasers_rect.append(rect)

        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)
        self.save_rect = []
        for (i, img) in enumerate(self.save_img):
            rect = pygame.Rect(830, 10 + i * 64, 64, 64)
            self.save_rect.append(rect)

        self.sizes = [
            pygame.image.load("img/加号.png").convert_alpha(),
            pygame.image.load("img/减号.png").convert_alpha()
        ]
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(138+60, 20 + i * 32, 32, 32)
            self.sizes_rect.append(rect)

    def generate_random_colors(self, num_colors=24):
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in
                       range(num_colors)]

    def set_brush(self, brush):
        self.brush = brush

    def draw(self):
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.erasers):
            self.screen.blit(img, self.erasers_rect[i].topleft)
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)

        for (i, img) in enumerate(self.save_img):
            self.screen.blit(img, self.save_rect[i].topleft)
        pygame.draw.rect(self.screen, (0, 0, 0), (180+80, 10, 64, 64), 1)
        size = self.brush.get_size()
        y = 10 + 32
        x = 180 + 110
        pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), int(size))
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

    def click_button(self, pos):
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:
                    self.brush.set_size(self.brush.get_size() - 0.5)
                else:
                    self.brush.set_size(self.brush.get_size() + 0.5)
                return True
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
        for (i, rect) in enumerate(self.erasers_rect):
            print("rect",rect)
            if rect.collidepoint(pos):
                print(123)
                self.brush.set_color(self.eraser_color)
                return True
        return False

class Paint:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((950, 600))
        pygame.display.set_caption("艺术画板V1.0")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)

    def clear_screen(self):
        self.screen.fill((255, 255, 255))

    def run(self):
        self.clear_screen()
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.clear_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] >= 74 and not self.menu.click_button(event.pos):
                        self.brush.start_draw(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.brush.drawing:
                        self.brush.draw(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.brush.end_draw()

            self.menu.draw()
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    paint = Paint()
    paint.run()
