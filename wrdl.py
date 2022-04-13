"""
Словце (Wordle)
@author: GvozdevRS
"""
import os
import random
import re

DIR = os.path.dirname(os.path.realpath(__file__))
# DICT_SOURCE_PATH = os.path.join(DIR, 'books', 'ozhegov.txt')
DICT_PATH = os.path.join(DIR, 'data', 'dictionary')
LETTERS = 5
MAX_GUESSES = 6


def main():
    # Dictionary.create_dictionary(DICT_SOURCE_PATH, DICT_PATH, LETTERS)
    dictionary = Dictionary(DICT_PATH)
    game = Game(dictionary, LETTERS, MAX_GUESSES)
    cli = CLI(game)
    cli.run()


class Dictionary:
    """Словарь для игры"""
    words = []

    def __init__(self, dict_path):
        """
        dict_path : str - путь к файлу словаря
        """
        self.load_dictionary(dict_path)

    def get_word(self):
        """Возвращает случайное слово из словаря"""
        random_word = random.choice(self.words)
        return random_word

    def word_exists(self, word):
        """Возвращает True, если слово есть в словаре"""
        if word in self.words:
            return True
        return False

    def load_dictionary(self, dict_path):
        """
        Загружает словарь из файла
        dict_path : str - путь к файлу словаря
        """
        with open(dict_path + str(LETTERS), encoding='utf-8') as file:
            self.words = file.read().split()

    @staticmethod
    def create_dictionary(source_path, dict_path, letters):
        """
        Создает словарь для игры из источника (книги)
        source_path : str - путь к входному файлу источника
        dict_path : str - путь к выходному файлу словаря
        letters : int - кол-во букв
        """
        words = set()
        with open(source_path) as file:
            reg_exp = fr" [А-ЯЁ]{{{letters}}}[ ,]"
            words_raw = re.findall(reg_exp, file.read())
            for word in words_raw:
                words.add(word[len(word)-letters-1: -1].lower())
        with open(dict_path + str(LETTERS), 'w+', encoding='utf-8') as file:
            for word in words:
                file.write(word + '\n')


class Game:
    """
    В игре Словце (Wordle) Вам необходимо угадать слово из {} букв
    На угадывание слова у Вас {} попыток
    """

    def __init__(self, dictionary, letters, max_guesses):
        """
        dictionary : Dictionary - словарь
        letters : int - кол-во букв в слове
        max_guesses : int - максимальное кол-во попыток
        """
        self.dictionary = dictionary
        self.letters = letters
        self.max_guesses = max_guesses
        self.reset()

    def reset(self):
        """Сброс переменных"""
        self.num_guesses = 1
        self.guessed_letters = ['?' for _ in range(self.letters)]

    def check_guess(self, guess, secret_word):
        """
        Проверяет догадку пользователя
        Возвращает строку с информацией о догадке (вида "+ - + - ~"), где:
        "+" - буква на позиции угадана
        "~" - буква в слове есть, но на другой позиции
        "-" - буквы в слове нет
        guess : str - догадка
        secret_word : str - секретное слово
        """
        if not self.dictionary.word_exists(guess):
            return 'Данное слово отсутствует в словаре!'
        if guess == secret_word:
            return f'Победа! | {self.num_guesses}/{self.max_guesses}'
        clues = list(guess)
        secret = list(secret_word)
        for i in range(self.letters):  # 1-ый проход - поиск совпадающих позиций
            if clues[i] == secret_word[i]:
                self.guessed_letters[i] = clues[i]
                secret.remove(clues[i])
                clues[i] = '+'
        for i in range(self.letters):  # 2-ой проход - остальные варианты
            if clues[i] in secret:
                secret.remove(clues[i])
                clues[i] = '~'
            elif clues[i] != '+':
                clues[i] = '-'
        self.num_guesses += 1
        return ' '.join(clues)


class CLI:
    """Консольный интерфейс (CLI) для игры Словце (Wordle)"""

    def __init__(self, game):
        """
        game : Game - объект игры
        """
        self.game = game

    def run(self):
        """Запуск игры в консоли"""
        print(self.game.__doc__.format(self.game.letters, self.game.max_guesses))
        while True:
            secret_word = self.game.dictionary.get_word()
            while True:
                guess = self.get_guess()
                print(' '.join([ch for ch in guess]))
                print(self.game.check_guess(guess, secret_word))
                if guess == secret_word:
                    break
                if self.game.num_guesses > self.game.max_guesses:
                    print('У Вас закончились попытки!')
                    print(f'Правильный ответ - {secret_word}')
                    break
            print('Хотите сыграть ещё раз?')
            if not input('Y/N:> ').upper().startswith('Y'):
                break
            self.game.reset()
        print('Спасибо за игру!')

    def get_guess(self):
        """Возвращает догадку пользователя"""
        print(' '.join(self.game.guessed_letters))
        prompt = '{}/{}:> '.format(self.game.num_guesses,
                                   self.game.max_guesses)
        guess = input(prompt)
        while len(guess) != self.game.letters:
            print('Некорректный ввод!')
            guess = input(prompt)
        return guess


if __name__ == '__main__':
    main()
