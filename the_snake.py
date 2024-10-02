from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    position = (320, 240)

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для переопределения в дочерних классах"""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним"""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.position = self.randomize_position()
        super().__init__(body_color)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        res = (randint(0, 31) * 20, randint(0, 23) * 20)
        return res

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение"""

    position = (320, 240)
    body_color = SNAKE_COLOR

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(body_color)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки"""
        head = self.positions[0]
        self.last = self.positions.pop()
        if self.direction == RIGHT:
            if head[0] == 620:
                new_head = (0, head[1])
            else:
                new_head = (head[0] + 20, head[1])
        elif self.direction == LEFT:
            if head[0] == 0:
                new_head = (620, head[1])
            else:
                new_head = (head[0] - 20, head[1])
        elif self.direction == DOWN:
            if head[1] == 460:
                new_head = (head[0], 0)
            else:
                new_head = (head[0], head[1] + 20)
        elif self.direction == UP:
            if head[1] == 0:
                new_head = (head[0], 460)
            else:
                new_head = (head[0], head[1] - 20)
        self.positions.insert(0, new_head)

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Начинает игру заново"""
        self.length = 1
        self.positions.clear()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def main():
    """Основаня функция запуска игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.last)
            new_position = apple.randomize_position()
            if new_position in snake.positions:
                while new_position in snake.positions:
                    new_position = apple.randomize_position()
            apple.position = new_position
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
