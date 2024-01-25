import pygame
import os
import Start_Window
import random


class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load('fonosnovnoi.jpg')  # Загрузка изображения фона

    def draw_background(self):
        self.screen.blit(self.bg_image, (0, 0))  # Отображение фона на экране


class Player:
    def __init__(self):
        self.rocket_lcoords = (180, 600)  # Координаты левого положения ракеты
        self.rocket_rcoords = (400, 600)  # Координаты правого положения ракеты
        self.images = []  # Список изображений для анимации игрока
        # Загрузка изображений для анимации игрока (псевдокод)
        for i in range(1, 5):
            image_path = os.path.join(f'space_ship{i}.png')
            self.images.append(pygame.image.load(image_path))
        self.index = 0  # Текущий индекс изображения
        self.image = self.images[self.index]  # Текущее изображение игрока
        self.rect = self.image.get_rect()  # Получение прямоугольника для коллизий
        self.rect.x, self.rect.y = self.rocket_lcoords
        self.animation_speed = 100  # Скорость анимации (меньшее значение – медленнее)
        self.move_direction = 1  # Направление перемещения игрока (1 - вправо, -1 - влево)

    def update(self):
        # Логика обновления анимации игрока
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def move(self):
        # Логика перемещения игрока при нажатии на пробел
        if self.move_direction == 1:
            self.rect.x, self.rect.y = self.rocket_rcoords
            self.move_direction = -1
        else:
            self.rect.x, self.rect.y = self.rocket_lcoords
            self.move_direction = 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Отображение игрока на экране


class Asteroids:
    def __init__(self, screen):
        self.screen = screen
        self.meteor_image = pygame.image.load(os.path.join('meteorite.png'))  # Изображение астероида
        self.meteor_lcoords = (180, -100)  # Координаты левой начальной позиции астероида
        self.meteor_rcoords = (400, -100)  # Координаты правой начальной позиции астероида
        self.meteor_speed = 5  # Скорость перемещения астероида вниз
        self.meteor_interval = 200  # Интервал между появлениями астероидов
        self.meteors = []  # Список всех астероидов

    def update(self, player_rect):
        for meteor in self.meteors.copy():
            meteor[1] += self.meteor_speed  # Перемещение астероида вниз

            if meteor[1] >= 800:  # Удаление астероида, если он вышел за пределы экрана
                self.meteors.remove(meteor)

        # Создание нового астероида через определенный интервал
        if len(self.meteors) == 0 or self.meteors[-1][1] >= self.meteor_interval:
            coords = random.choice([self.meteor_lcoords, self.meteor_rcoords])
            self.meteors.append([pygame.Rect(coords, (64, 64)), -100])

        # Проверка на столкновение астероида с игроком
        for meteor in self.meteors:
            if meteor[1] >= 600 and player_rect.colliderect(meteor[0]):
                game_over(self.screen)  # Вызов функции game_over
                break

    def draw(self):
        for meteor in self.meteors:
            self.screen.blit(self.meteor_image, meteor[0])  # Отображение астероида на экране


def game_over(screen):
    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отображение изображения game_over.png
    game_over_image = pygame.image.load(os.path.join('data', 'game_over.png'))
    screen.blit(game_over_image, (0, 0))

    # Создание кнопки "Играть"
    play_button = pygame.Rect(200, 400, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_button)  # Отрисовка кнопки
    font = pygame.font.Font(None, 36)
    play_text = font.render('Играть', True, (0, 0, 0))
    screen.blit(play_text, (250, 410))

    # Создание кнопки "Меню"
    menu_button = pygame.Rect(200, 500, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), menu_button)  # Отрисовка кнопки
    menu_text = font.render('Меню', True, (0, 0, 0))
    screen.blit(menu_text, (260, 510))

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
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    clock = pygame.time.Clock()

    # Создание объектов игрового окна, игрока и астероидов
    game_window = GameWindow(screen)
    player = Player()
    asteroids = Asteroids(screen)

    game_overfl = False
    while not game_overfl:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_overfl = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.move()

        game_window.draw_background()  # Отображение фона
        asteroids.update(player.rect)  # Обновление состояния астероидов
        player.update()  # Обновление состояния игрока
        asteroids.draw()  # Отображение астероидов
        player.draw(screen)  # Отображение игрока

        pygame.display.flip()  # Обновление экрана
        clock.tick(30)  # Ограничение кадров в секунду (30 FPS)


if __name__ == "__main__":
    pygame.init()  # Инициализация Pygame
    play()  # Вызов функции для запуска игры
    pygame.quit()  # Завершение Pygame
