# Разработать игру.
# Примеры игр:
# пинг-понг
# змейка
# тетрис
# игра на выживание с постоянным передвижением, где на поле постоянно появляются “враги”,
# которых нельзя касаться

import pygame
import random

# Инициализация pygame
pygame.init()

# Настройки игрового окна
screen_width, screen_height = 300, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Настройки цветов
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
colors = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0),
          (128, 0, 128), (0, 255, 0), (255, 0, 0), gray]

# Настройки игровых параметров
clock = pygame.time.Clock()
fps = 5

speed = 5

# Параметры игрового поля
columns, rows = 10, 20
cell_size = 30
board_width = cell_size * columns
board_height = cell_size * rows

# Инициализация игрового поля
board = [[black for _ in range(columns)] for _ in range(rows)]

#grid = [[0 for _ in range(board_width)] for _ in range(board_height)]

# grid_size = 20
# grid_width = screen_width // grid_size
# grid_heigth = screen_height // grid_size

# Описываем формы фигур
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Инициализация игрового поля
#grid = [[0 for _ in range(grid_width)] for _ in range(grid_heigth)]


# Класс для управления фигурами
class Piece(object):
    #rows = grid_heigth  # 20
    #columns = grid_width  # 10 ???

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        self.rotation = 0


# Функция для создания новой фигуры
def create_piece():
    return Piece(0, 0, random.choice(shapes))

# Функция отрисовки одного квадратика из фигуры
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

# Функция отрисовки фигуры
def draw_shape(x, y, piece):
    for yy, row in enumerate(piece.shape):
        for xx, block in enumerate(row):
            if block != 0: # не рисовать пустые квадратики
                draw_block(x + xx * cell_size, y + yy * cell_size, piece.color)

# Функция для проверки возможности движения или вращения
def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(board_width) if grid[i][j] == 0] for i in range(board_width)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted_piece = convert_piece_format(piece)

    for pos in formatted_piece:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


# Функция для конвертации формата фигуры
def convert_piece_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    return positions


# Функция отрисовки окна
# def draw_window(surface, grid):
#     surface.fill(black)
#
#     for i, row in enumerate(grid):
#         for j, column in enumerate(row):
#             #pygame.draw.rect(surface, colors[column], (j * grid_size, i * grid_size, grid_size, grid_size), 0)
#             pygame.draw.rect(surface, gray, (j * grid_size, i * grid_size, grid_size, grid_size), 0)
#
#     pygame.display.update()

def draw_board(surface):
    for y in range(rows):
        for x in range(columns):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, board[y][x], rect)
            pygame.draw.rect(surface, gray, rect, 1)

# def stop_down():
#     pass
#
# def check_collision(shape, offset, game_field):
#     offset_x, offset_y = offset
#
#     # (field_height, field_width) - размеры игрового поля
#     field_height = len(game_field)
#     field_width = len(game_field[0])
#
#     for y, row in enumerate(shape):
#         for x, cell in enumerate(row):
#             if cell:  # Если в текущей ячейке фигуры есть блок
#                 # Рассчитываем позицию этого блока на игровом поле
#                 pos_x = offset_x + x
#                 pos_y = offset_y + y
#                 # Проверяем, не выходит ли блок за границы поля
#                 if pos_x < 0 or pos_x >= field_width or pos_y < 0 or pos_y >= field_height:
#                     return True  # Столкновение с границами поля
#                 if game_field[pos_y][pos_x]:  # Если ячейка не пуста
#                     return True  # Столкновение с другой фигурой
#     return False

def fix_piece(x, y, piece):
    for yy, row in enumerate(piece.shape):
        for xx, block in enumerate(row):
            if block != 0: # не фиксировать пустые квадратики
                board[x+xx][y+yy] = piece.color

def control_stop(piece):
    res = False
    print(piece.y)
    for yy, row in enumerate(piece.shape):
        for xx, block in enumerate(row):
            if block != 0: # не рисовать пустые квадратики
                #draw_block(x + xx * cell_size, y + yy * cell_size, piece.color)
                new_y = piece.y + 1
                print(new_y)
                if new_y >= board_height:
                    res = True
                    break
                elif board[piece.x][new_y] != (0, 0 ,0): # надо остановить
                    res = True
                    break
    res = False # не надо останавливать -> двигаем дальше вниз

    return res

def control_row(num_row):
    for j in range(0, columns-1):
        if board[num_row][j] == (0, 0 , 0):
            return False
    return True

def remove_row(num_row):
    for i in range(num_row, 1, -1): # удаление нижней строки -> сдвинуть все строки вниз
        for j in range(0, columns-1):
            board[i][j] = board[i-1][j]
    for j in range(0, columns-1): # очистить верхнюю строку
        board[0][j] = (0, 0, 0)
# def control_board():
#     for i in range(rows-1, 0, -1):
#         if True:
#             pass

pygame.display.set_caption('Тетрис')
# Основной игровой цикл
def main():
    run = True
    current_piece = create_piece()
    print(f"{current_piece.x}  - {current_piece.y} ")
    print(current_piece.shape)
    print(board)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Переместить фигуру влево
                    current_piece.x -= cell_size
                elif event.key == pygame.K_RIGHT:
                    # Переместить фигуру вправо
                    current_piece.x += cell_size
                elif event.key == pygame.K_DOWN:
                    # Ускорить падение фигуры
                    pass
                    # fix_piece(current_piece.x, current_piece.y, current_piece)
                elif event.key == pygame.K_UP:
                    # Повернуть фигуру
                    #current_piece = rotate(current_piece)
                    #convert_piece_format(current_piece)
                    pass

        draw_board(screen)
        draw_shape(current_piece.x, current_piece.y, current_piece)
        if current_piece.y == 30:
            #fix_piece(current_piece.x, current_piece.y, current_piece)
            run = False
            print(board)
        print(f"{current_piece.x} - {current_piece.y}")
        pygame.display.flip()
        clock.tick(fps)

        current_piece.y += cell_size

    pygame.quit()


main()