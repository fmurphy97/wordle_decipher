from collections import Counter
from itertools import chain
import random


class WordDecipher:

    def __init__(self, filtered_list):
        self.unfiltered_list = filtered_list
        self.filtered_list = filtered_list
        self.complete = False
        self.won = 0
        self.attempt = 0

        max_size = int(0.03 * len(five_word_list))
        secret_word = random.choice(five_word_list[:max_size])
        self.secret_word = secret_word


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
        # check that the amount of times that the character is in green + yellow >= times in th input word
        list_to_return2 = list_to_return
        if letter_correct_frequency > 1:
            list_to_return2 = []
            for word in list_to_return:
                letter_appearances1 = Counter(chain.from_iterable(word))
                if character in letter_appearances1.keys():
                    if letter_appearances1[character] >= letter_correct_frequency:
                        list_to_return2.append(word)

        self.filtered_list = list_to_return2

    def rule_gray(self, character, total_appearances, yellow_appearances, total_positions, yellow_positions,
                  position):
        list_to_return = []


        if total_appearances > 0:

            for word in self.filtered_list:
                counter = True
                for lno, letter in enumerate(word):
                    if (letter == character) and (lno not in total_positions):
                        counter = False
                        break
                if counter:
                    list_to_return.append(word)
            self.filtered_list = list_to_return

        if yellow_appearances > 0:
            list_to_return = []
            for word in self.filtered_list:
                counter = True
                for lno, letter in enumerate(word):
                    if (letter == character) and (lno == position):
                        counter = False
                        break
                if counter:
                    list_to_return.append(word)
            self.filtered_list = list_to_return

        elif total_appearances == 0:
            list_to_return = []
            for word in self.filtered_list:
                counter = True
                for lno, letter in enumerate(word):
                    if letter == character:
                        counter = False
                        break
                if counter:
                    list_to_return.append(word)
            self.filtered_list = list_to_return

    def word_to_functions(self, word, word_correctness):
        word_correctness_list = [int(x) for x in list(str(word_correctness))]

        # Calculate amount of greens/yellow in other places
        green_appearances = {letter: 0 for letter in word}
        total_positions = {letter: [-1] for letter in word}
        yellow_appearances = {letter: 0 for letter in word}
        yellow_positions = {letter: [-1] for letter in word}
        total_appearances = {letter: 0 for letter in word}

        for lno, letter in enumerate(word):
            i = word_correctness_list[lno]
            if i > 0:
                count = total_positions[letter]
                count.append(lno)
                total_positions[letter] = count
                total_appearances[letter] += 1
                if i == 1:
                    yellow_appearances[letter] += 1
                    count_yellow = total_positions[letter]
                    count_yellow.append(lno)
                    yellow_positions[letter] = count_yellow


        for lno, letter in enumerate(word):
            if word_correctness_list[lno] == 0:
                self.rule_gray(character=letter, position=lno, total_appearances=total_appearances[letter],
                               yellow_appearances=yellow_appearances[letter],
                               total_positions=total_positions[letter], yellow_positions=yellow_positions[letter])
            elif word_correctness_list[lno] == 1:
                self.rule_yellow(character=letter, position=lno, letter_correct_frequency=total_appearances[letter])
            elif word_correctness_list[lno] == 2:
                self.rule_green(letter, lno)

    def filtered_list_small(self, amount):
        dif = len(self.filtered_list) - amount
        if dif > 0:
            return f'{self.filtered_list[:10]} ...and {dif} more'
        else:
            return self.filtered_list

    def reset_file(self):
        self.filtered_list = self.unfiltered_list
        self.complete = False
        self.attempt = 0

        max_size = int(0.03 * len(five_word_list))
        secret_word = random.choice(five_word_list[:max_size])
        self.secret_word = secret_word

    def run_game(self):
        word = 'carie'
        while not self.complete:
            result = self.make_output(word)
            correctness = "".join([str(x) for x in result])
            self.word_to_functions(word=word, word_correctness=correctness)
            word = self.check_victory(result)
        # replay = input("Press (y)es to play again, (n)o to exit")
        # if replay == 'y':
        #     self.reset_file()
        #     self.run_game()

#    if (letter == character) and (lno not in green_positions) and (lno not in yellow_positions):
#TypeError: argument of type 'NoneType' is not iterable
    def check_victory(self, result):
        score = sum(result)
        if self.attempt == 6 and score < 5 * 2:
            print(f'You loose, the word was {self.secret_word}')
            self.complete = True
        elif self.attempt == 6:
            self.complete = True
        if score == 5 * 2:
            print(f'You won!. The secret word was {self.secret_word}')
            self.complete = True
            self.won = 1
        self.attempt += 1

        if not self.complete:
            suggested_word = self.filtered_list[0]
            print(f'Word:{suggested_word}')
            return suggested_word

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



if __name__ == '__main__':
    input_file = open('sorted_words.json', "r", encoding='utf-8')
    word_list_string = input_file.read()
    five_word_list = eval(word_list_string)
    input_file.close()

    wins = []
    tries = []

    for i in range(1000):
        try:
            game = WordDecipher(five_word_list)
            game.run_game()
            if game.won == 1:
                tries.append(game.attempt)
                wins.append(1)
            else:
                wins.append(0)
        except:
            pass
