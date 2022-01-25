from collections import Counter
from itertools import chain
from wordle_decipher.word_cleanup import create_input_list
from wordle_decipher.config import WORD_SIZE, LANGUAGE


class WordDecipher:

    def __init__(self, filtered_list, word_length):
        self.unfiltered_list = filtered_list
        self.filtered_list = filtered_list
        self.complete = False
        self.word_length = word_length

    def rule_green(self, character, position):
        list_to_return = []
        for word in self.filtered_list:
            if word[position] == character:
                list_to_return.append(word)
        self.filtered_list = list_to_return

    def rule_yellow(self, character, position, letter_correct_frequency):
        list_to_return = []
        # check the values that contain the letter but not in that position
        for word in self.filtered_list:
            for lno, letter in enumerate(word):
                if (lno != position) and (letter == character) and (word[position] != character):
                    list_to_return.append(word)
                    break

        # check that the amount of times that the character is in green + yellow >= times in the input word
        list_to_return2 = list_to_return
        if letter_correct_frequency > 1:
            list_to_return2 = []
            for word in list_to_return:
                letter_appearances1 = Counter(chain.from_iterable(word))
                if character in letter_appearances1.keys():
                    if letter_appearances1[character] >= letter_correct_frequency:
                        list_to_return2.append(word)

        self.filtered_list = list_to_return2

    def rule_gray(self, character, letter_correct_frequency, position):
        list_to_return = []

        if letter_correct_frequency > 0:
            for word in self.filtered_list:
                counter = True
                for lno, letter in enumerate(word):
                    if (letter == character) and (lno == position):
                        counter = False
                        break
                if counter:
                    list_to_return.append(word)
            self.filtered_list = list_to_return

        else:
            for word in self.filtered_list:
                counter = True
                for lno, letter in enumerate(word):
                    if letter == character:
                        counter = False
                        break
                if counter:
                    list_to_return.append(word)
            self.filtered_list = list_to_return

    def filter_possible_results(self, word, word_correctness):
        word_correctness_list = [int(x) for x in list(str(word_correctness))]

        # Calculate amount of greens/yellow in other places
        total_appearances = {letter: 0 for letter in set(word)}
        for letter, letter_correctness in zip(word, word_correctness_list):
            if letter_correctness > 0:
                total_appearances[letter] += 1

        for lno, letter in enumerate(word):
            # print(f'The len was {len(self.filtered_list)} before using letter {letter}')
            if word_correctness_list[lno] == 0:
                self.rule_gray(character=letter, position=lno, letter_correct_frequency=total_appearances[letter])
            elif word_correctness_list[lno] == 1:
                self.rule_yellow(character=letter, position=lno, letter_correct_frequency=total_appearances[letter])
            elif word_correctness_list[lno] == 2:
                self.rule_green(letter, lno)
            # print(f'The len was {len(self.filtered_list)} after using letter {letter}')

    def filtered_list_small(self, amount):
        dif = len(self.filtered_list) - amount
        if dif > 0:
            return f'{self.filtered_list[:10]} ...and {dif} more'
        else:
            return self.filtered_list

    def reset_word_decipher(self):
        self.filtered_list = self.unfiltered_list
        self.complete = False

    def input_word(self):
        while True:
            word = input("Enter chosen word:  ").strip().lower()
            if len(word) != self.word_length:
                print(f"Sorry, word length must be {self.word_length}.")
                continue
            elif word not in self.unfiltered_list:
                print("Sorry, word must be in the dictionary.")
                continue
            else:
                break
        return word

    def input_correctness_vector(self):
        correctness = ""
        request_input = True
        while request_input:
            correctness = input("Enter 0/1/2 string:  ")

            if len(correctness) != self.word_length:
                print(f"Sorry, number vector length must be {self.word_length}.")
                continue
            else:
                counter = 0
                for num in correctness:
                    if num not in {"0", "1", "2"}:
                        counter += 1
                        print("Sorry, numbers must be 0, 1 or 2.")
                        break
                if counter == 0:
                    request_input = False
        return correctness

    def run_word_decipher(self):
        while not self.complete:
            word = self.input_word()
            correctness = self.input_correctness_vector()

            self.filter_possible_results(word=word, word_correctness=correctness)
            print(f'Possible words:{self.filtered_list_small(amount=10)}')
            if len(self.filtered_list) <= 1:
                self.complete = True
        self.reset_word_decipher()
        input("Press enter to exit")


if __name__ == '__main__':
    dictionary_word_list = create_input_list(word_length=WORD_SIZE, language=LANGUAGE)
    game = WordDecipher(dictionary_word_list, word_length=WORD_SIZE)
    game.run_word_decipher()
