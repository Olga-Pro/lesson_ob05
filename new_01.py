import pygame
import random

# Инициализация pygame
pygame.init()

# Настройки игрового окна
screen_width, screen_height = 400, 600
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

# Параметры игрового поля
columns, rows = 10, 20
cell_size = 30
board_width = cell_size * columns
board_height = cell_size * rows

# Инициализация игрового поля
board = [[black for _ in range(columns)] for _ in range(rows)]

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

# Класс для управления фигурами
class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        # self.rotation = 0

    def rotate_shape(self):
        # повернуть фигуру
        self.shape = [ [ self.shape[y][x] for y in range(len(self.shape)) ] for x in range(len(self.shape[0]) - 1, -1, -1) ]

    def on_bottom(self, board_height):
        # достигли дна
        if (self.y + cell_size * len(self.shape)) >= board_height:
            return True
        else:
            return False

    def on_left_board(self):
        # достигли левого края
        if (self.x - cell_size) < 0:
            return True
        else:
            return False
    def on_right_board(self, board_width):
        # достигли правого края
        if (self.x + cell_size * len(self.shape[0])) >= board_width:
            return True
        else:
            return False

    def valid_space(self, l_r):
        # проверить пространство для фигуры на игровом поле
        x_shape = self.x // cell_size + l_r
        y_shape = self.y // cell_size + 1

        for yy, row in enumerate(self.shape):
            for xx, block in enumerate(row):
                if block != 0:  # не рисовать пустые квадратики
                    if y_shape + yy >= rows or x_shape + xx >= columns:
                        return False
                    elif board[y_shape + yy][x_shape + xx] != (0, 0, 0):
                        return False
        return True

    def save_on_board(self, x, y):
        # сохранить фигуру на игровом поле
        x_shape = x // cell_size
        y_shape = y // cell_size
        #print(f"y={y} y_shape = {y_shape}")
        #board[yy][xx] = colors[shapes.index(self.shape)]#self.shape
        #print(board[y_shape])
        for yy, row in enumerate(self.shape):
            for xx, block in enumerate(row):
                #print(f"xx={xx} yy={yy}")
                if block != 0:  # не рисовать пустые квадратики
                    #print(self.shape)
                    board[y_shape+yy][x_shape+xx] = self.color
                    #print(board[y_shape+yy])



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

# Функция для отрисовки экрана и сетки
def draw_board(surface):
    for y in range(rows):
        for x in range(columns):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, board[y][x], rect)
            pygame.draw.rect(surface, gray, rect, 1)

def remove_row(num_row):
    for i in range(num_row, 1, -1):  # удаление строки -> сдвинуть все строки вниз
        for j in range(0, columns - 1):
            board[i][j] = board[i - 1][j]
    for j in range(0, columns - 1):  # очистить верхнюю строку
        board[0][j] = (0, 0, 0)

def full_row():
    # проверка заполненности строки и удаление заполненной
    for yy, row in enumerate(board):
        res = 0
        for xx, block in enumerate(row):
            if board[yy][xx] != (0, 0, 0):
                res += 1
        if res == columns:
            remove_row(yy)




pygame.display.set_caption('Тетрис')
# Основной игровой цикл
def main():
    run = True
    current_piece = create_piece()

    #print(f"{current_piece.x}  - {current_piece.y} ")
    #print(current_piece.shape)
    #print(board)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Переместить фигуру влево
                    if not current_piece.on_left_board() and not current_piece.on_bottom(board_height) and current_piece.valid_space(-1):
                        current_piece.x -= cell_size
                elif event.key == pygame.K_RIGHT:
                    # Переместить фигуру вправо
                    if not current_piece.on_right_board(board_width) and not current_piece.on_bottom(board_height) and current_piece.valid_space(1):
                        current_piece.x += cell_size
                elif event.key == pygame.K_DOWN:
                    # Ускорить падение фигуры
                    while current_piece.valid_space(0) and not current_piece.on_bottom(board_height):
                        # пока есть пространство - двигаем вниз
                        current_piece.y += cell_size
                elif event.key == pygame.K_UP:
                    # Повернуть фигуру
                    rotate_piece = current_piece
                    rotate_piece.rotate_shape()
                    if rotate_piece.valid_space(0):
                        current_piece = rotate_piece


        draw_board(screen)
        draw_shape(current_piece.x, current_piece.y, current_piece)
        full_row()

        if not current_piece.on_bottom(board_height) and current_piece.valid_space(0):
            # если не дно и есть пространство - едем вниз
            current_piece.y += cell_size
        else:
            current_piece.save_on_board(current_piece.x, current_piece.y)
            current_piece = create_piece()
            # проверить заполненность игрового поля
            if not current_piece.valid_space(0):
                print("Игра окончена")
                run = False

        print(f"{current_piece.x} - {current_piece.y}")
        pygame.display.flip()
        clock.tick(fps)

        #current_piece.y += cell_size

    pygame.quit()


main()

# # [1[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  2[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  3[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  4[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  5[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  6[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  7[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  8[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  9[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  10[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  1[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  2[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  3[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  4[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  5[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  6[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  7[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  8[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  9[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
#  20[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]]