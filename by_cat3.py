import pygame
import sys

# Инициализация Pygame
pygame.init()

# Окно приложения
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Падение фигуры")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Параметры фигуры
x = 350
y = 50
width_rect = 20
height_rect = 100
velocity = 0
gravity = 0.5


# Функция отрисовки фигуры
def draw_figure(x, y, width, height):
    pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, width, height))


running = True
while running:
    screen.fill(BLACK)

    # Проверяем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновляем положение фигуры
    y += velocity
    velocity += gravity

    # Проверка столкновения с "полом"
    if y + height_rect >= height:
        y = height - height_rect
        velocity = 0

    # Отрисовываем фигуру
    draw_figure(x, y, width_rect, height_rect)

    pygame.display.flip()  # обновление содержимого всего экрана
    pygame.time.Clock().tick(60)  # ограничение кадров в секунду

pygame.quit()
sys.exit()