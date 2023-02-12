import pygame
import sys
import random
import time


class Game():
    def __init__(self):
        # задаем размеры экрана
        self.screen_width = 500
        self.screen_height = 530

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        self.BLUE = pygame.Color(0, 0, 255)

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        self.new_game()

    def new_game(self):
        self.play_surface.fill(self.white)
        self.score = 0
        self.snake = Snake(self.green)
        self.food = Food(self.brown, self.screen_width, self.screen_height)
        self.big_food = False

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        """Задаем surface(поверхность поверх которой будет все рисоваться)
        и устанавливаем загаловок окна"""
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')

    def event_loop(self, change_to):
        """Функция для отслеживания нажатий клавиш игроком"""

        # запускаем цикл по ивентам
        for event in pygame.event.get():
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def refresh_screen(self):
        """обновляем экран и задаем фпс"""
        pygame.display.flip()
        game.fps_controller.tick(23)

    def show_score(self, choice=1):
        """Отображение результата"""
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_overe отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (360, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.new_game()
                        running = False
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
        pygame.display.flip()


class Snake():
    def __init__(self, snake_color):
        # важные переменные - позиция головы змеи и его тела
        self.snake_head_pos = [100, 50]  # [x, y]
        self.rect = pygame.Rect(*self.snake_head_pos, 10, 10)
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # направление движение змеи, изначально
        # зададимся вправо
        self.direction = "RIGHT"
        # куда будет меняться напрвление движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction

    def validate_direction_and_change(self):
        """Изменияем направление движения змеи только в том случае,
        если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Изменияем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
            self.rect.x += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
            self.rect.x -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
            self.rect.y -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10
            self.rect.y += 10

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        # если вставлять просто snake_head_pos,
        # то на всех трех позициях в snake_body
        # окажется один и тот же список с одинаковыми координатами
        # и мы будем управлять змеей из одного квадрата
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            food_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]
            score += 1
        elif game.big_food and self.snake_head_pos == game.big_food.food_pos:
            score += game.big_food.radius
            game.big_food = False
        else:
            # если не нашли еду, то убираем последний сегмент,
            # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        """Отображаем все сегменты змеи"""
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            # pygame.Rect(x,y, sizex, sizey)
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        """Проверка, что столкунлись с концами экрана или сами с собой
        (змея закольцевалась)"""
        if self.snake_head_pos[0] >= screen_width + 10:
            self.snake_head_pos[0] = 0
        if self.snake_head_pos[0] <= -10:
            self.snake_head_pos[0] = screen_width
        if self.snake_head_pos[1] >= screen_height + 10:
            self.snake_head_pos[1] = 0
        if self.snake_head_pos[1] <= -10:
            self.snake_head_pos[1] = screen_height
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()

        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        """Инит еды"""
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                         random.randrange(1, screen_height/10)*10]

    def draw_food(self, play_surface):
        """Отображение еды"""
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


class Big_food():
    def __init__(self):
        #инит большой бонусной еды, очки приносит, на прирост не влияет, со временем "тает", соответственно очков меньше
        self.previouos_score = game.score
        self.radius = 15
        self.food_pos = [random.randrange(1, game.screen_width / 10) * 10,
                         random.randrange(1, game.screen_height / 10) * 10]
        self.rect = pygame.Rect(*self.food_pos, 10, 10)

    def update(self):
        if self.radius == 0:
            game.big_food = False
        if game.score - self.previouos_score == 1:
            self.radius -= 5
            self.previouos_score = game.score
        pygame.draw.circle(game.play_surface, game.BLUE, self.food_pos, self.radius)


class Wall():
    def __init__(self, x_pos, y_pos):
        self.pos = (x_pos, y_pos)
        self.size = (10, 10)
        self.rect = pygame.Rect((self.pos[0], self.pos[1], *self.size))

    def draw_rect(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)


game = Game()
game.new_game()
game.init_and_check_for_errors()
game.set_surface_and_title()

walls = []
with open("levels/level 1", 'r', encoding="utf-8") as level_file:
    reader = level_file.readlines()
    x, y = 0, 30
    for line in reader:
        line = line.rstrip()
        for rect in line:
            if rect == '#':
                walls.append(Wall(x, y))
            x += 50
        y += 50
        x = 0


while True:
    game.snake.change_to = game.event_loop(game.snake.change_to)

    game.snake.validate_direction_and_change()
    game.snake.change_head_position()
    game.score, game.food.food_pos = game.snake.snake_body_mechanism(
        game.score, game.food.food_pos, game.screen_width, game.screen_height)
    game.snake.draw_snake(game.play_surface, game.white)

    game.food.draw_food(game.play_surface)
    if game.big_food:
        game.big_food.update()

    game.snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)

    for wall in walls:
        wall.draw_rect(game.play_surface)

    game.show_score()
    game.refresh_screen()
    if not game.big_food and random.randrange(101) < 1:
        game.big_food = Big_food()