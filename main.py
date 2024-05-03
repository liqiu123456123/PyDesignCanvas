# -*- coding: utf-8 -*-
import math
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
class Brush:
    """
    画笔类
    """
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
        for i in range(self.brush.get_width()):
            for j in range(self.brush.get_height()):
                self.brush.set_at((i, j), color + (self.brush.get_at((i, j)).a,))

    def get_color(self):
        return self.color

    def draw(self, pos):
        if self.drawing: # 判断是否开始绘画
            for p in self._get_points(pos):
                pygame.draw.circle(self.screen, self.color, p, int(self.size))
            self.last_pos = pos # 记录画笔最后位置

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
    """
    菜单类
    """
    def __init__(self, screen):
        self.screen = screen  # 初始化窗口
        self.brush = None
        self.colors = [
            (0xff, 0x00, 0x00),  # 红色
            (0xff, 0x80, 0x00),  # 橙色
            (0xff, 0xff, 0x00),  # 黄色
            (0x00, 0xff, 0x00),  # 绿色
            (0x00, 0xff, 0x80),  # 青色
            (0x00, 0x00, 0xff),  # 蓝色
            (0x80, 0x00, 0xff),  # 紫色
            (0xff, 0x00, 0xff),  # 品红色
            (0xc0, 0xc0, 0xc0),  # 银色
            (0x80, 0x80, 0x80),  # 灰色
            (0x40, 0x40, 0x40),  # 深灰色
            (0x00, 0x00, 0x00),  # 黑色

            # 添加更多颜色
            (0xff, 0x40, 0x00),  # 深红色
            (0xff, 0xa0, 0x00),  # 浅橙色
            (0xff, 0xff, 0x80),  # 浅黄色
            (0x00, 0xff, 0x40),  # 深绿色
            (0x00, 0x80, 0xff),  # 深蓝色
            (0x80, 0x40, 0xff),  # 深紫色
            (0xff, 0x40, 0xff),  # 深品红色
            (0xe0, 0xe0, 0xe0),  # 浅银色
            (0xa0, 0xa0, 0xa0),  # 浅灰色
            (0x60, 0x60, 0x60),  # 中灰色

            # 继续添加
            (0xff, 0x00, 0x80),  # 玫瑰红
            (0xff, 0x00, 0x40),  # 栗色
            (0xff, 0xc0, 0x00),  # 金色
            (0x80, 0xff, 0x00),  # 黄绿色
            (0x00, 0xff, 0xc0),  # 孔雀蓝
            (0x00, 0x40, 0xff),  # 靛蓝
            (0xc0, 0x00, 0xff),  # 深品红
            (0xff, 0xc0, 0xff),  # 浅粉色
            (0x90, 0x90, 0x90),  # 中性灰
            (0x30, 0x30, 0x30),  # 暗灰色

            # 更多颜色
            (0x40, 0x80, 0x00),  # 橄榄色
            (0x80, 0x40, 0x00),  # 褐色
            (0x80, 0xff, 0x80),  # 淡青色
            (0x00, 0x80, 0x80),  # 浅蓝色
        ]
        self.eraser_color = (0xff, 0xff, 0xff) # 初始颜色
        # 计算每个色块在画板中的坐标值，便于绘制
        self.colors_rect = []
        x_start = 364  # 起始x坐标
        y_start = 10  # 起始y坐标
        width = 32  # 方块宽度
        height = 32  # 方块高度
        spacing = 2  # 方块之间的间隔

        # 假设有3行12列的颜色方块
        rows = 3
        cols = 12

        for i in range(len(self.colors)):
            # 计算x和y坐标
            x = x_start + (i % cols) * (width + spacing)  # 计算列位置
            y = y_start + (i // cols) * (height + spacing)  # 计算行位置

            # 创建一个矩形对象
            rect = pygame.Rect(x, y, width, height)
            self.colors_rect.append(rect)
        self.pens = [  # 画笔图片
            pygame.image.load("img/画笔.png").convert_alpha(),
        ]
        self.erasers = [  # 橡皮图片
            pygame.image.load("img/橡皮擦.png").convert_alpha(),
        ]
        self.save_img = [  # 橡皮图片
            pygame.image.load("img/保存.png").convert_alpha(),
        ]

        self.erasers_rect = []
        for (i, img) in enumerate(self.erasers):  # 橡皮列表
            rect_x = 10 + (i + 1) * 64  # 假设x坐标保持不变，与画笔相同布局
            rect_y = 10  # 假设从屏幕底部某个位置开始放置橡皮擦
            rect = pygame.Rect(rect_x+30, rect_y + i * 64, 64, 64)  # 垂直布局，每个橡皮擦相隔64像素
            self.erasers_rect.append(rect)

        self.pens_rect = []
        for (i, img) in enumerate(self.pens):  # 画笔列表
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)
        self.save_rect = []
        for (i, img) in enumerate(self.save_img):  # 画笔列表
            rect = pygame.Rect(830, 10 + i * 64, 64, 64)
            self.save_rect.append(rect)

        self.sizes = [  # 加减号图片
            pygame.image.load("img/加号.png").convert_alpha(),
            pygame.image.load("img/减号.png").convert_alpha()
        ]

        # 计算坐标，便于绘制
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(138+60, 20 + i * 32, 32, 32)
            self.sizes_rect.append(rect)

    def set_brush(self, brush):  # 设置画笔对象
        self.brush = brush

    def draw(self):  # 绘制菜单栏
        for (i, img) in enumerate(self.pens): # 绘制画笔样式按钮
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.erasers): # 绘制橡皮按钮
            self.screen.blit(img, self.erasers_rect[i].topleft)
        for (i, img) in enumerate(self.sizes): # 绘制 + - 按钮
            self.screen.blit(img, self.sizes_rect[i].topleft)

        for (i, img) in enumerate(self.save_img): # 绘制 + - 按钮
            self.screen.blit(img, self.save_rect[i].topleft)
        # 绘制用于实时展示画笔的小窗口

        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (180+80, 10, 64, 64), 1)
        size = self.brush.get_size()
        y = 10 + 32
        x = 180 + 110
        # 在窗口中展示画笔
        pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), int(size))
        for (i, rgb) in enumerate(self.colors): # 绘制色块
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

    def click_button(self, pos):
        # 点击加减号事件
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:  # i == 1, size down
                    self.brush.set_size(self.brush.get_size() - 0.5)
                else:
                    self.brush.set_size(self.brush.get_size() + 0.5)
                return True
        # 点击颜色按钮事件
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
        # 点击橡皮按钮事件
        for (i, rect) in enumerate(self.erasers_rect):
            print("rect",rect)
            if rect.collidepoint(pos):
                print(123)
                self.brush.set_color(self.eraser_color)
                return True
        return False

class Paint:
    """
    窗口绘制类
    """

    def __init__(self):
        pygame.init()  # 初始化pygame库
        self.screen = pygame.display.set_mode((950, 600))  # 显示窗口
        pygame.display.set_caption("艺术画板V1.0")  # 设置窗口标题
        self.clock = pygame.time.Clock()  # 控制速率
        self.brush = Brush(self.screen)  # 创建画刷对象
        self.menu = Menu(self.screen)  # 创建窗口菜单
        self.menu.set_brush(self.brush)  # 设置默认画刷

    def clear_screen(self):
        self.screen.fill((255, 255, 255))  # 填充空白

    def run(self):
        self.clear_screen()  # 清除屏幕
        running = True  # 添加一个变量来控制主循环
        while running:
            # 设置fps，表示每秒执行30次（注意：30不是毫秒数）
            self.clock.tick(30)
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == QUIT:  # 退出事件
                    running = False  # 退出主循环
                elif event.type == KEYDOWN:  # 按键事件
                    if event.key == K_ESCAPE:  # ESC按键事件
                        self.clear_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标左键按下事件
                    if event.pos[0] >= 74 and not self.menu.click_button(event.pos):  # 未点击画板按钮
                        self.brush.start_draw(event.pos)  # 开始绘画
                elif event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
                    if self.brush.drawing:  # 假设Brush类有一个is_drawing属性
                        self.brush.draw(event.pos)  # 绘画动作
                elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标左键松开事件
                    self.brush.end_draw()  # 停止绘画

            self.menu.draw()
            pygame.display.flip()  # 使用flip更新整个屏幕，这比update更高效

        pygame.quit()  # 退出pygame

if __name__ == '__main__':
    # 创建Paint类的对象
    paint = Paint()
    paint.run()  # 启动主窗口
