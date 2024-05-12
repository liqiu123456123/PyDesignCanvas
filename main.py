# -*- coding: utf-8 -*-
import math
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import random


class Brush:
    def __init__(self, screen):
        """
        Brush 类的构造函数，用于初始化画笔

        参数:
        screen (pygame.Surface): 绘制表面
        """
        self.screen = screen  # 绘制表面
        self.color = (0, 0, 0)  # 画笔颜色，默认为黑色
        self.size = 1  # 画笔大小
        self.drawing = False  # 是否正在绘画
        self.last_pos = None  # 上一个绘制点的位置
        self.space = 1  # 画笔间距（在原始代码中未使用）

        # 加载画笔图像并设置默认大小为1x1（实际上可能是用于绘制时的图标或光标）
        self.brush = pygame.image.load("img/画笔.png").convert_alpha()
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))

        # 开始绘画

    def start_draw(self, pos):
        """
        开始绘画操作

        参数:
        pos (tuple): 起始点的坐标（x, y）
        """
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        """
        结束绘画操作
        """
        self.drawing = False

    def get_current_brush(self):
        """
        获取当前使用的画笔（或称为光标）图像

        返回:
        pygame.Surface: 当前画笔图像
        """
        return self.brush_now

    def set_size(self, size):
        """
        设置画笔大小

        参数:
        size (float): 画笔大小，范围在0.5到32之间
        """
        if size < 0.5:
            size = 0.5
        elif size > 32:
            size = 32
        self.size = size
        # 更新画笔图像的子表面大小
        self.brush_now = self.brush.subsurface((0, 0), (int(size * 2), int(size * 2)))

    def get_size(self):
        """
        获取画笔大小

        返回:
        float: 当前画笔大小
        """
        return self.size

    def set_color(self, color):
        """
        设置画笔颜色

        参数:
        color (tuple): RGB颜色值，如(255, 0, 0)表示红色
        """
        self.color = color

    def get_color(self):
        """
        获取画笔颜色

        返回:
        tuple: 当前画笔颜色
        """
        return self.color

    def draw(self, pos):
        """
        在屏幕上绘制点

        参数:
        pos (tuple): 要绘制的点的坐标（x, y）
        """
        if self.drawing:
            # 注意：_get_points(pos) 这个方法没有在代码中定义，这里假设它返回一系列点
            for p in self._get_points(pos):
                pygame.draw.circle(self.screen, self.color, p, int(self.size))
            self.last_pos = pos  # 更新上一个绘制点的位置

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
        # 初始化菜单，传入窗口表面作为参数
        self.screen = screen
        self.brush = None  # 画笔对象，稍后由Paint类设置

        # 生成随机颜色（虽然此处并未在__init__中显示生成过程，但假设有generate_random_colors方法）
        self.generate_random_colors()

        # 设置橡皮擦颜色为白色
        self.eraser_color = (0xff, 0xff, 0xff)

        # 存储颜色矩形的列表
        self.colors_rect = []

        # 初始化颜色矩形的位置和大小
        x_start = 364
        y_start = 10
        width = 32
        height = 32
        spacing = 2
        cols = 12

        # 遍历颜色列表（尽管在__init__中没有显示，但假设self.colors是一个包含颜色的列表）
        for i in range(len(self.colors)):
            x = x_start + (i % cols) * (width + spacing)
            y = y_start + (i // cols) * (height + spacing)
            rect = pygame.Rect(x, y, width, height)
            self.colors_rect.append(rect)

            # 加载画笔图片并转换为包含alpha通道的表面
        self.pens = [
            pygame.image.load("img/画笔.png").convert_alpha(),
        ]

        # 加载橡皮擦图片并转换为包含alpha通道的表面
        self.erasers = [
            pygame.image.load("img/橡皮擦.png").convert_alpha(),
        ]

        # 加载保存图片并转换为包含alpha通道的表面
        self.save_img = [
            pygame.image.load("img/保存.png").convert_alpha(),
        ]

        # 存储橡皮擦矩形的列表
        self.erasers_rect = []
        for (i, img) in enumerate(self.erasers):
            rect_x = 10 + (i + 1) * 64
            rect_y = 10
            rect = pygame.Rect(rect_x + 30, rect_y + i * 64, 64, 64)
            self.erasers_rect.append(rect)

            # 存储画笔矩形的列表
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)

            # 存储保存图片矩形的列表
        self.save_rect = []
        for (i, img) in enumerate(self.save_img):
            rect = pygame.Rect(830, 10 + i * 64, 64, 64)
            self.save_rect.append(rect)

            # 加载调整画笔大小的图片并转换为包含alpha通道的表面
        self.sizes = [
            pygame.image.load("img/加号.png").convert_alpha(),
            pygame.image.load("img/减号.png").convert_alpha()
        ]

        # 存储调整画笔大小按钮的矩形列表
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(138 + 60, 20 + i * 32, 32, 32)
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
        # 初始化pygame库
        pygame.init()

        # 设置窗口大小并创建窗口
        self.screen = pygame.display.set_mode((950, 600))

        # 设置窗口标题
        pygame.display.set_caption("艺术画板V1.0")

        # 创建一个时钟对象，用于控制游戏循环的帧率
        self.clock = pygame.time.Clock()

        # 创建一个画笔对象，并传入窗口表面作为参数
        self.brush = Brush(self.screen)

        # 创建一个菜单对象，并传入窗口表面作为参数
        self.menu = Menu(self.screen)

        # 将画笔对象传递给菜单对象，用于设置画笔属性（例如颜色、大小等）
        self.menu.set_brush(self.brush)

    def clear_screen(self):
        # 清除屏幕，用白色填充
        self.screen.fill((255, 255, 255))

    def run(self):
        # 清除屏幕开始绘制
        self.clear_screen()

        # 运行标志，默认为True，表示程序正在运行
        running = True

        # 游戏主循环
        while running:
            # 控制帧率，限制循环每秒运行30次
            self.clock.tick(30)

            # 遍历所有pygame事件
            for event in pygame.event.get():
                # 如果事件是退出事件
                if event.type == pygame.QUIT:  # 注意这里应该是pygame.QUIT而不是QUIT
                    running = False
                    # 如果事件是键盘按下事件
                elif event.type == pygame.KEYDOWN:  # 注意这里应该是pygame.KEYDOWN而不是KEYDOWN
                    # 如果按下的是ESC键
                    if event.key == pygame.K_ESCAPE:  # 注意这里应该是pygame.K_ESCAPE而不是K_ESCAPE
                        self.clear_screen()
                        # 如果事件是鼠标按下事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 如果鼠标位置在菜单之外，并且没有点击到菜单按钮
                    if event.pos[0] >= 74 and not self.menu.click_button(event.pos):
                        self.brush.start_draw(event.pos)
                        # 如果事件是鼠标移动事件
                elif event.type == pygame.MOUSEMOTION:
                    # 如果画笔正在绘制
                    if self.brush.drawing:
                        self.brush.draw(event.pos)
                        # 如果事件是鼠标释放事件
                elif event.type == pygame.MOUSEBUTTONUP:
                    # 结束绘制
                    self.brush.end_draw()

                    # 绘制菜单
            self.menu.draw()

            # 更新窗口显示
            pygame.display.flip()

            # 退出pygame
        pygame.quit()

if __name__ == '__main__':
    paint = Paint()
    paint.run()
