import pygame
import os
import random
import Start_Window

meteor_lcoords = (160, -50)
meteor_rcoords = (380, -50)
screen = pygame.display.set_mode((600, 800))
score = 0


class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load('E:/pygm1/data/fonosnovnoi.jpg')  # Загрузка изображения фона

    def draw_background(self):
        self.screen.blit(self.bg_image, (0, 0))  # Отображение фона на экране


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rocket_lcoords = (180, 600)
        self.rocket_rcoords = (400, 600)
        self.images = [pygame.image.load(os.path.join('data', f'space_ship{i}.png')) for i in range(1, 5)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.rocket_lcoords
        self.rocket_animation_speed = 30  # Скорость анимации
        self.move_direction = 1

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def move(self):
        if self.move_direction == 1:
            self.rect.x, self.rect.y = self.rocket_rcoords
            self.move_direction = -1
        else:
            self.rect.x, self.rect.y = self.rocket_lcoords
            self.move_direction = 1


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, meteor_image, meteor_speed, meteor_interval):
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', meteor_image))
        self.rect = self.image.get_rect()
        self.meteor_lcoords = (160, 0)
        self.meteor_rcoords = (380, 0)
        self.rect.x, self.rect.y = random.choice([self.meteor_lcoords, self.meteor_rcoords])
        self.speed = meteor_speed
        self.interval = meteor_interval

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.kill()  # Удаление спрайта, если он выходит за пределы экрана

    def check_collision(self, player):
        global screen
        if pygame.sprite.collide_rect(self, player):
            game_over(screen)


def game_over(screen):
    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отображение изображения game_over.png
    game_over_image = pygame.image.load(os.path.join('data', 'game_over.png'))
    screen.blit(game_over_image, (0, 0))

    # Создание кнопки "Играть"
    play_button = pygame.Rect(200, 670, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_button)  # Отрисовка кнопки
    font = pygame.font.Font(None, 36)
    play_text = font.render('Заново', True, (0, 0, 0))
    screen.blit(play_text, (250, 680))

    # Создание кнопки "Меню"
    menu_button = pygame.Rect(200, 730, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), menu_button)  # Отрисовка кнопки
    menu_text = font.render('Меню', True, (0, 0, 0))
    screen.blit(menu_text, (260, 740))

    pygame.display.flip()  # Обновление экрана

    # Ожидание действий пользователя
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button.collidepoint(x, y):
                    play()  # Вызов функции для запуска игры
                elif menu_button.collidepoint(x, y):
                    Start_Window.main()  # Вызов функции для возвращения в меню


# Основной игровой цикл
def play():
    global score
    global meteor_lcoords
    global meteor_rcoords
    pygame.init()
    clock = pygame.time.Clock()

    # Создание объектов игрового окна, игрока и астероидов
    game_window = GameWindow(screen)
    player = Player()
    asteroids = Asteroid('meteorite.png', 15, 30)

    asteroid_group = pygame.sprite.Group()
    asteroid_group.add(asteroids)

    spawn_counter = 0  # Счетчик для отслеживания появления новых астероидов
    spawn_interval = 500  # Set the interval for spawning asteroids
    last_spawn_time = pygame.time.get_ticks()  # Initialize the time of the last spawn

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.move()

        # Создавать астероиды через регулярные промежутки времени
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval:
            new_asteroid = Asteroid('meteorite.png', 15, 30)
            new_asteroid.rect.x = random.choice(
                [meteor_lcoords[0], meteor_rcoords[0]])  # Установить начальную позицию x
            asteroid_group.add(new_asteroid)
            last_spawn_time = current_time  # Обновить время последнего появления
            score += 1
        screen.fill((0, 0, 0))  # Очистка экрана
        game_window.draw_background()  # Отображение фона

        player.update()
        asteroid_group.update()

        # Проверка столкновения астероидов с игроком
        for asteroid in asteroid_group:
            asteroid.check_collision(player)

        asteroid_group.draw(screen)  # Отображение астероидов
        screen.blit(player.image, player.rect)  # Отображение игрока

        pygame.display.flip()  # Обновление экрана
        clock.tick(60)  # Ограничение частоты кадров

    pygame.quit()
