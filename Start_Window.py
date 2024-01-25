import pygame
import os
import sys

import game_window

pygame.init()


class Start:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.black = (0, 0, 0)
        self.font1 = pygame.font.Font(None, 26)
        self.screen = pygame.display.set_mode((width, height))
        self.data_folder = os.path.join(os.path.dirname(__file__))
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(self.data_folder, "data/fongame.jpg")),
                                                 (width, height))
        self.icon = pygame.image.load(os.path.join(self.data_folder, "data/icon.jpg"))
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Switch!')
        self.start_button = pygame.Rect(200, 680, 200, 50)
        self.exit_button = pygame.Rect(200, 740, 200, 50)

    def draw_start_button(self):
        pygame.draw.rect(self.screen, (0, 128, 255), self.start_button)
        font = pygame.font.Font(None, 36)
        text = font.render('Начать', True, (255, 255, 255))
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)

    def draw_exit_button(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button)
        font = pygame.font.Font(None, 36)
        text = font.render('Выход', True, (255, 255, 255))
        text_rect = text.get_rect(center=self.exit_button.center)
        self.screen.blit(text, text_rect)

    def draw_rules(self):
        file_path = os.path.join(self.data_folder, 'data/rules.txt')
        rules = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    rules.append(line.strip())
        except FileNotFoundError:
            print("Файл не найден")
        except Exception as e:
            print("Произошла ошибка при чтении файла:", e)

        y_offset = 30
        for rule in rules:
            text = self.font1.render(rule, True, (255, 255, 255))
            self.screen.blit(text, (30, y_offset))
            y_offset += 40  # Увеличиваем вертикальный отступ для следующей строки


def main():
    # Создание объекта игры
    start = Start(600, 800)

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Выход из программы при нажатии на кнопку "выход"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.start_button.collidepoint(event.pos):
                    game_window.play()

        start.screen.blit(start.background, (0, 0))  # Отображение фона

        start.draw_start_button()  # Отображение кнопки "Начать"
        start.draw_exit_button()  # Отображение кнопки "Выход"
        start.draw_rules()
        pygame.display.flip()  # Обновление экрана

    # Завершение Pygame
    pygame.quit()


if __name__ == '__main__':
    main()