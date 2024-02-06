import pygame
import os
import random
import Start_Window

meteor_lcoords = (160, -50)
meteor_rcoords = (350, -50)
screen = pygame.display.set_mode((600, 800))
score = 0


class GameWindow:
    def __init__(self, screen):
        global score
        self.screen = screen
        self.font_score = pygame.font.Font("data/Maji.ttf", 100)
        self.bg_image = pygame.image.load('data/fonosnovnoi.jpg')  # Загрузка изображения фона

    def draw_background(self):
        self.screen.blit(self.bg_image, (0, 0))  # Отображение фона на экране

    def draw_score(self, score):
        text = self.font_score.render(f'{score}', True, (0, 255, 0))  # Update the score in the text
        self.screen.blit(text, (30, 80))  # Adjust the position as required


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rocket_lcoords = (200, 600)
        self.rocket_rcoords = (400, 600)
        self.images = [pygame.image.load(os.path.join('data', f'space_ship{i}.png')) for i in range(1, 5)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.rocket_lcoords
        self.rocket_animation_speed = 30  # Скорость анимации
        self.move_direction = 1

    def update(self):  # Анимация
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def move(self):  # Перемещение
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
        self.meteor_rcoords = (350, 0)
        self.rect.x, self.rect.y = random.choice([self.meteor_lcoords, self.meteor_rcoords])
        self.speed = meteor_speed
        self.interval = meteor_interval

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.kill()  # Удаление спрайта, если он выходит за пределы экрана

    def check_collision(self, player):  # Проверка на столкновение с астероидом
        global screen
        if pygame.sprite.collide_rect(self, player):
            game_over(screen)


def game_over(screen):
    global score

    font_score = pygame.font.Font("data/Maji.ttf", 100)

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отображение изображения game_over.png
    game_over_image = pygame.image.load(os.path.join('data', 'game_over.png'))
    screen.blit(game_over_image, (0, 0))

    # Вывод конечного счета
    font_text_score = pygame.font.Font("data/Sriracha.ttf", 60)
    text = font_text_score.render('YOUR SCORE:', True, (128, 0, 0))
    screen.blit(text, (60, 440))
    text = font_score.render(f"{score}", True, (255, 0, 0))
    screen.blit(text, (425, 440))
    # Создание кнопки "Заново"
    play_button = pygame.Rect(200, 670, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_button)  # Отрисовка кнопки
    font_text = pygame.font.Font("data/Arkhip.ttf", 36)
    play_text = font_text.render('Заново', True, (0, 0, 0))
    text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, text_rect)

    # Создание кнопки "Меню"
    menu_button = pygame.Rect(200, 730, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), menu_button)  # Отрисовка кнопки
    menu_text = font_text.render('Меню', True, (0, 0, 0))
    screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))

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
                    score = 0
                    play_1()  # Вызов функции для запуска игры
                elif menu_button.collidepoint(x, y):
                    score = 0
                    Start_Window.main()  # Вызов функции для возвращения в меню
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_2:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.5)
                elif event.key == pygame.K_3:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(1)


# Основной игровой цикл
def play_1():
    global score
    global meteor_lcoords
    global meteor_rcoords

    # Флаг для паузы музыки
    music_flag = 0

    clock = pygame.time.Clock()

    # Создание объектов игрового окна, игрока и астероидов
    game_window = GameWindow(screen)

    player = Player()
    asteroids = Asteroid('meteorite_2.png', 10, 40)

    asteroid_group = pygame.sprite.Group()
    asteroid_group.add(asteroids)

    spawn_interval = 900  # Установите интервал появления астероидов
    last_spawn_time = pygame.time.get_ticks()  # Инициализируем время последнего появления

    # Надпись "SCORE"
    font_text_score = pygame.font.Font("data/Sriracha.ttf", 50)
    text = font_text_score.render('SCORE:', True, (255, 255, 255))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.move()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    if music_flag == 0:
                        pygame.mixer.music.pause()
                        music_flag = 1
                    else:
                        pygame.mixer.music.unpause()
                        music_flag = 0
                elif event.key == pygame.K_2:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.5)
                elif event.key == pygame.K_3:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(1)
        # Создавать астероиды через регулярные промежутки времени
        current_time = pygame.time.get_ticks()
        if score >= 50:
            play_2()
        if current_time - last_spawn_time > spawn_interval:
            new_asteroid = Asteroid('meteorite_2.png', 10, 40)
            new_asteroid.rect.x = random.choice(
                [meteor_lcoords[0], meteor_rcoords[0]])  # Установить начальную позицию x
            asteroid_group.add(new_asteroid)
            last_spawn_time = current_time  # Обновить время последнего появления
            score += 1
        screen.fill((0, 0, 0))  # Очистка экрана
        game_window.draw_background()  # Отображение фона
        game_window.draw_score(score)  # Отображение счета
        player.update()
        asteroid_group.update()

        # Проверка столкновения астероидов с игроком
        for asteroid in asteroid_group:
            asteroid.check_collision(player)

        asteroid_group.draw(screen)  # Отображение астероидов
        screen.blit(player.image, player.rect)  # Отображение игрока
        screen.blit(text, (30, 20))  # Отображение надписи "SCORE"
        pygame.display.flip()  # Обновление экрана
        clock.tick(60)  # Ограничение частоты кадров


def play_2():
    global score
    global meteor_lcoords
    global meteor_rcoords

    # Флаг для паузы музыки
    music_flag = 0
    clock = pygame.time.Clock()

    # Создание объектов игрового окна, игрока и астероидов
    game_window = GameWindow(screen)
    player = Player()
    asteroids = Asteroid('meteorite.png', 15, 30)

    asteroid_group = pygame.sprite.Group()
    asteroid_group.add(asteroids)

    spawn_interval = 500  # Установите интервал появления астероидов
    last_spawn_time = pygame.time.get_ticks()  # Инициализируем время последнего появления

    # Надпись "SCORE"
    font_text_score = pygame.font.Font("data/Sriracha.ttf", 50)
    text = font_text_score.render('SCORE:', True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.move()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    if music_flag == 0:
                        pygame.mixer.music.pause()
                        music_flag = 1
                    else:
                        pygame.mixer.music.unpause()
                        music_flag = 0
                elif event.key == pygame.K_2:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.5)
                elif event.key == pygame.K_3:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(1)
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
        game_window.draw_score(score)  # Отображение счета
        player.update()
        asteroid_group.update()

        # Проверка столкновения астероидов с игроком
        for asteroid in asteroid_group:
            asteroid.check_collision(player)

        asteroid_group.draw(screen)  # Отображение астероидов
        screen.blit(player.image, player.rect)  # Отображение игрока
        screen.blit(text, (30, 20))  # Отображение надписи "SCORE"
        pygame.display.flip()  # Обновление экрана
        clock.tick(60)  # Ограничение частоты кадров
