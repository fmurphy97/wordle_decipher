from collections import Counter
import random


class WordGame:

    def __init__(self, filtered_list):
        self.unfiltered_list = filtered_list
        self.filtered_list = filtered_list
        self.complete = False
        self.attempt = 0

        max_size = int(0.03 * len(five_word_list))
        secret_word = random.choice(five_word_list[:max_size])
        self.secret_word = secret_word

    def run(self):
        while not self.complete:
            while True:
                word = input("Enter chosen word:  ").strip().lower()
                if word not in self.filtered_list or len(word) != 5:
                    print('Word must be in dictionary and have 5 characters')
                    continue
                else:
                    break
            result = self.make_output(word)
            self.check_victory(result)
        replay = input("Press (y)es to play again, (n)o to exit")
        if replay == 'y':
            self.reset_file()
            self.run()

    def reset_file(self):
        self.filtered_list = self.unfiltered_list
        self.complete = False
        self.attempt = 0
        max_size = int(0.03 * len(five_word_list))
        secret_word = random.choice(five_word_list[:max_size])
        self.secret_word = secret_word

    def check_victory(self, result):
        score = sum(result)
        if self.attempt == 6 and score < 5 * 2:
            print(f'You loose, the word was {self.secret_word}')
            self.complete = True
        elif self.attempt == 6:
            self.complete = True
        elif score == 5 * 2:
            print('You win')
            self.complete = True
        self.attempt += 1

    def make_output(self, word):
        result, iw_remaining_letters, sw_remaining_letters = self.check_green(word)
        result = self.check_yellow(word, result, iw_remaining_letters, sw_remaining_letters)
        print(result)
        return result

    def check_green(self, word):
        result = [0 for x in range(5)]
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


instructions = 'Adivina la palabra en seis intentos.' \
               '\nCada intento debe ser una palabra válida de 5 letras. Pulsa ENTER para enviar.' \
               '\nDespués de cada intento el color de las letras cambia para mostrar qué ' \
               'tan cerca estás de acertar la palabra.}' \
               '\n Cada vez que se inserta una palabra muestra un 2 si la letra esta ' \
               'en la palabra y en la posición correcta.' \
               '\n Muestra un 1 si la letra está en la palabra pero en la posición incorrecta.' \
               '\n Muestra un 0 si la letra no está en la palabr.' \
               '\n---------------------------------------------------------------------------------------------------' \
               '\n'

if __name__ == '__main__':
    input_file = open('sorted_words.json', "r", encoding='utf-8')
    word_list_string = input_file.read()
    five_word_list = eval(word_list_string)
    input_file.close()

    game = WordGame(five_word_list)
    print(instructions)
    game.run()
