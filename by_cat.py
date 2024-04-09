import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Тетрис')

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Параметры игрового поля
COLUMNS, ROWS = 10, 20
CELL_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = CELL_SIZE * COLUMNS, CELL_SIZE * ROWS
board = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]


# Функция для отрисовки игрового поля
def draw_board(surface):
    for y in range(ROWS):
        for x in range(COLUMNS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, board[y][x], rect)
            pygame.draw.rect(surface, GRAY, rect, 1)


# Основной игровой цикл
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    # Отрисовка игрового поля
    draw_board(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()


# Этот код создает базовую структуру для игры в (Тетрис, но
# в нем отсутствуют ключевые механики, такие
# как генерация тетромино, обработка столкновений, вращение
# и устранение заполненных линий. Для добавления этих механик
# вам потребуется дополнительно создать систему управления
# фигурами, включая их формы, повороты и управление столкновениями
# между фигурами и краями игрового поля.
# Тетрис является отличным учебным проектом, который поможет вам
# лучше понять основы программирования и работы с графикой в (Python.
# Удачи с разработкой!