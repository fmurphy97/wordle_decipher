from collections import Counter
import random
from word_cleanup import create_input_list
from config import WORD_SIZE, LANGUAGE

class WordGame:

    MAX_ATTEMPTS = 6

    def __init__(self, filtered_list, word_length):
        self.unfiltered_list = filtered_list
        self.filtered_list = filtered_list
        self.complete = False
        self.attempt = 0
        self.won = False
        self.secret_word = ""
        self.word_length = word_length

    def run_game(self):
        self.reset_game()
        while not self.complete:
            while True:
                word = input("Enter chosen word:  ").strip().lower()
                if word not in self.filtered_list or len(word) != self.word_length:
                    print(f'Word must be in dictionary and have {self.word_length} characters')
                    continue
                else:
                    break
            result = self.make_output(word)
            self.check_victory(result)
        replay = input("Press (y)es to play again, (n)o to exit")
        if replay == 'y':
            self.run_game()

    def reset_game(self):
        self.filtered_list = self.unfiltered_list
        self.complete = False
        self.attempt = 0
        max_size = int(0.05 * len(self.unfiltered_list))
        secret_word = random.choice(self.unfiltered_list[:max_size])
        self.secret_word = secret_word
        self.won = False

    def check_victory(self, result):
        self.attempt += 1
        score = sum(result)

        if self.attempt == self.MAX_ATTEMPTS:
            self.complete = True
            if score < self.word_length * 2:
                print(f'You loose, the word was {self.secret_word}')
        if score == self.word_length * 2 and self.attempt <= self.MAX_ATTEMPTS:
            print(f'You won in {self.attempt} tries')
            self.complete = True
            self.won = True

    def make_output(self, word):
        result, iw_remaining_letters, sw_remaining_letters = self.check_green(word)
        result = self.check_yellow(word, result, iw_remaining_letters, sw_remaining_letters)
        print(result)
        return result

    def check_green(self, word):
        result = [0 for x in range(self.word_length)]
        iw_remaining_letters = list(word)
        sw_remaining_letters = list(self.secret_word)
        for lno, letter in enumerate(word):
            if letter == self.secret_word[lno]:
                result[lno] = 2
                iw_remaining_letters.remove(letter)
                sw_remaining_letters.remove(letter)
        return result, iw_remaining_letters, sw_remaining_letters

    def check_yellow(self, word, result, iw_remaining_letters, sw_remaining_letters):
        iw_letter_counter = Counter(iw_remaining_letters)
        sw_letter_counter = Counter(sw_remaining_letters)
        for letter in iw_letter_counter.keys():
            if letter in sw_letter_counter.keys():
                contador = 0
                for lno, letter2 in enumerate(word):
                    if contador == min(sw_letter_counter[letter], iw_letter_counter[letter]):
                        break
                    if result[lno] == 0 and letter == letter2:
                        contador += 1
                        result[lno] = 1

        return result



if __name__ == '__main__':
    dictionary_word_list = create_input_list(word_length=WORD_SIZE, language=LANGUAGE)
    game = WordGame(dictionary_word_list, word_length=WORD_SIZE)
    # instructions = 'Adivina la palabra en seis intentos.' \
    #                f'\nCada intento debe ser una palabra válida de {game.word_length} letras. Pulsa ENTER para enviar.' \
    #                '\nDespués de cada intento el color de las letras cambia para mostrar qué ' \
    #                'tan cerca estás de acertar la palabra.' \
    #                '\nCada vez que se inserta una palabra muestra un 2 si la letra esta ' \
    #                'en la palabra y en la posición correcta.' \
    #                '\n Muestra un 1 si la letra está en la palabra pero en la posición incorrecta.' \
    #                '\n Muestra un 0 si la letra no está en la palabra.' \
    #                '\n---------------------------------------------------------------------------------------------------' \
    #                '\n'
    # print(instructions)
    game.run_game()
