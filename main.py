import pygame
import random

# Инициализация pygame
pygame.init()

# Константы

# Настройки игрового окна
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600

# Параметры игрового поля
COLUMNS, ROWS = 10, 20
CELL_SIZE = 30
BOARD_WIDTH = CELL_SIZE * COLUMNS
BOARD_HEIGTH = CELL_SIZE * ROWS

# Настройки цветов
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
colors = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0),
          (128, 0, 128), (0, 255, 0), (255, 0, 0), gray]


# Описываем формы фигур
SHAPES = [
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
        self.color = colors[SHAPES.index(shape)]

    def rotate_shape(self):
        # повернуть фигуру
        self.shape = [ [ self.shape[y][x] for y in range(len(self.shape)) ] for x in range(len(self.shape[0]) - 1, -1, -1) ]

    def on_bottom(self):
        # достигли дна?
        if (self.y + CELL_SIZE * len(self.shape)) >= BOARD_HEIGTH:
            return True
        else:
            return False

    def on_left_board(self):
        # достигли левого края?
        if (self.x - CELL_SIZE) < 0:
            return True
        else:
            return False

    def on_right_board(self):
        # достигли правого края?
        if (self.x + CELL_SIZE * len(self.shape[0])) >= BOARD_WIDTH:
            return True
        else:
            return False

    def valid_space(self, Board, l_r):
        # проверить пространство для фигуры на игровом поле
        x_shape = self.x // CELL_SIZE + l_r
        y_shape = self.y // CELL_SIZE + 1

        for yy, row in enumerate(self.shape):
            for xx, block in enumerate(row):
                if block != 0:  # не рисовать пустые квадратики
                    if y_shape + yy >= ROWS or x_shape + xx >= COLUMNS:
                        return False
                    elif Board.board[y_shape + yy][x_shape + xx] != (0, 0, 0):
                        return False
        return True

    def save_on_board(self, Board, x, y):
        # сохранить фигуру на игровом поле
        x_shape = x // CELL_SIZE
        y_shape = y // CELL_SIZE

        for yy, row in enumerate(self.shape):
            for xx, block in enumerate(row):
                if block != 0:  # не рисовать пустые квадратики
                    Board.board[y_shape+yy][x_shape+xx] = self.color

class Board():
    def __init__(self):
        # Инициализация игрового поля
        self.board = [[black for _ in range(COLUMNS)] for _ in range(ROWS)]

    # Функция для отрисовки экрана и сетки
    def draw_board(self, surface):
        for y in range(ROWS):
            for x in range(COLUMNS):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, self.board[y][x], rect)
                pygame.draw.rect(surface, gray, rect, 1)

    # Функция отрисовки одного квадратика из фигуры
    def draw_block(self, x, y, color, screen):
        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

    # Функция отрисовки фигуры
    def draw_shape(self, x, y, piece, screen):
        for yy, row in enumerate(piece.shape):
            for xx, block in enumerate(row):
                if block != 0:  # не рисовать пустые квадратики
                    self.draw_block(x + xx * CELL_SIZE, y + yy * CELL_SIZE, piece.color, screen)

    def remove_row(self, num_row):
        # удаление строки -> сдвинуть все строки вниз
        for i in range(num_row, 1, -1):
            for j in range(0, COLUMNS - 1):
                self.board[i][j] = self.board[i - 1][j]
        for j in range(0, COLUMNS - 1):  # очистить верхнюю строку
            self.board[0][j] = (0, 0, 0)

    def full_row(self):
        # проверка заполненности строки и удаление заполненной
        for yy, row in enumerate(self.board):
            res = 0
            for xx, block in enumerate(row):
                if self.board[yy][xx] != (0, 0, 0):
                    res += 1
            if res == COLUMNS:
                self.remove_row(yy)


class Game():
    def __init__(self):
        self.board = Board()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    def start(self):
        pass





def create_piece():
    return Piece(0, 0, random.choice(SHAPES))


game = Game()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Настройки игровых параметров
clock = pygame.time.Clock()
fps = 5

pygame.display.set_caption('Тетрис')
# Основной игровой цикл
def main():
    # game = Game()
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    run = True
    current_piece = create_piece()


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Переместить фигуру влево
                    if not current_piece.on_left_board() and not current_piece.on_bottom() and current_piece.valid_space(game.board, -1):
                        current_piece.x -= CELL_SIZE
                elif event.key == pygame.K_RIGHT:
                    # Переместить фигуру вправо
                    if not current_piece.on_right_board() and not current_piece.on_bottom() and current_piece.valid_space(game.board, 1):
                        current_piece.x += CELL_SIZE
                elif event.key == pygame.K_DOWN:
                    # Ускорить падение фигуры
                    while current_piece.valid_space(game.board, 0) and not current_piece.on_bottom():
                        # пока есть пространство - двигаем вниз
                        current_piece.y += CELL_SIZE
                elif event.key == pygame.K_UP:
                    # Повернуть фигуру
                    rotate_piece = current_piece
                    rotate_piece.rotate_shape()
                    if rotate_piece.valid_space(game.board, 0):
                        current_piece = rotate_piece

        game.board.draw_board(game.screen)
        game.board.draw_shape(current_piece.x, current_piece.y, current_piece, game.screen)
        game.board.full_row()

        if not current_piece.on_bottom() and current_piece.valid_space(game.board, 0):
            # если не дно и есть пространство - едем вниз
            current_piece.y += CELL_SIZE
        else:
            current_piece.save_on_board(game.board, current_piece.x, current_piece.y)
            current_piece = create_piece()
            # проверить заполненность игрового поля
            if not current_piece.valid_space(game.board, 0):
                print("Игра окончена")
                run = False

        #print(f"{current_piece.x} - {current_piece.y}")
        pygame.display.flip()
        clock.tick(fps)

        #current_piece.y += cell_size

    pygame.quit()


main()

