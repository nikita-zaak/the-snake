from random import choice, randint

import pygame

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
CENTER_POSITION: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)

BOARD_BACKGROUND_COLOR: tuple = (0, 0, 0)
BORDER_COLOR: tuple = (93, 216, 228)
APPLE_COLOR: tuple = (255, 0, 0)
SNAKE_COLOR: tuple = (0, 255, 0)

SPEED: int = 20

DIRECTION_MAP: dict = {
    (pygame.K_UP, DOWN): UP,
    (pygame.K_DOWN, UP): DOWN,
    (pygame.K_LEFT, RIGHT): LEFT,
    (pygame.K_RIGHT, LEFT): RIGHT,
}

screen: pygame.Surface = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)


pygame.display.set_caption('Змейка')


clock: pygame.time.Clock = pygame.time.Clock()


class GameObject:
    """Общий родитель для всех игровых объектов."""

    def __init__(
            self,
            body_color=(0, 0, 0),
            position=CENTER_POSITION
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color) -> None:
        """Рисует одну ячейку по заданным координатам."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Отрисовывает объект на экране."""


class Apple(GameObject):
    """Яблоко — игровой объект, который появляется в случайной точке."""

    def __init__(self) -> None:
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(
            self, 
            occupied_positions: list | None = None
    ) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        if occupied_positions is None:
            occupied_positions = [CENTER_POSITION]
        while True:
            random_x = randint(0, GRID_WIDTH - 1)
            random_y = randint(0, GRID_HEIGHT - 1)
            new_position = (random_x * GRID_SIZE, random_y * GRID_SIZE)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Игровой персонаж, управляемый с клавиатуры."""

    def __init__(self) -> None:
        super().__init__(SNAKE_COLOR)
        self.reset()

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction: tuple) -> None:
        """Обновляет направление движения."""
        self.direction = new_direction

    def move(self) -> None:
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        dx *= GRID_SIZE
        dy *= GRID_SIZE
        new_x = (head_x + dx) % SCREEN_WIDTH
        new_y = (head_y + dy) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        self.draw_cell(self.get_head_position(), self.body_color)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            new_direction = DIRECTION_MAP.get(
                (event.key, game_object.direction)
            )
            if new_direction:
                game_object.update_direction(new_direction)


def main() -> None:
    """Запускает игру и управляет игровым процессом."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с собой:
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
