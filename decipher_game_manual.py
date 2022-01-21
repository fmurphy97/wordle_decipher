from collections import Counter
from itertools import chain


class WordDecipher:

    def __init__(self, filtered_list):
        self.unfiltered_list = filtered_list
        self.filtered_list = filtered_list
        self.complete = False
        self.attempt = 0

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

    def rule_gray(self, character, green_appearances, yellow_appearances, green_positions, yellow_positions,
                  position):
        list_to_return = []
        if green_appearances > 0:
            for word in self.filtered_list:
                counter = True
                for lno, letter in enumerate(word):
                    if (letter == character) and (lno not in green_positions) and (lno not in yellow_positions):
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

        elif (yellow_appearances + green_appearances) == 0:
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
        green_appearances = {letter: 0 for letter in list(word)}
        green_positions = {letter: [] for letter in list(word)}
        yellow_appearances = {letter: 0 for letter in list(word)}
        yellow_positions = {letter: [] for letter in list(word)}
        total_appearances = {letter: 0 for letter in list(word)}

        for lno, letter in enumerate(word):
            i = word_correctness_list[lno]
            if i == 2:
                green_appearances[letter] += 1
                try:
                    green_positions[letter] = (green_positions[letter].append(lno))
                except AttributeError:
                    green_positions[letter] = [lno]
                total_appearances[letter] += 1
            elif i == 1:
                yellow_appearances[letter] += 1
                try:
                    yellow_positions[letter] = (yellow_positions[letter].append(lno))
                except AttributeError:
                    green_positions[letter] = [lno]
                total_appearances[letter] += 1

        for lno, letter in enumerate(word):
            if word_correctness_list[lno] == 0:
                self.rule_gray(character=letter, position=lno, green_appearances=green_appearances[letter],
                               yellow_appearances=yellow_appearances[letter],
                               green_positions=green_positions[letter], yellow_positions=yellow_positions[letter])
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

    def check_victory(self):
        self.attempt += 1
        if len(self.filtered_list) == 1:
            self.complete = True
            print(f'Congratulations, you won! The final word was {self.filtered_list[0]}')
        if self.attempt >= 6 and len(self.filtered_list) > 1:
            print('Sadly, you lost')

        if not self.complete:
            print('Here is a list of the suggested words:')
            print(self.filtered_list_small(amount=10))
            # print(f'The most likely ones are: {self.filtered_list[:3]}')

    def reset_file(self):
        self.filtered_list = self.unfiltered_list
        self.complete = False
        self.attempt = 0

    def run(self):
        while not self.complete:
            while True:
                word = input("Enter chosen word:  ").strip().lower()
                if len(word) != 5:
                    print("Sorry, word length must be 5.")
                    continue
                else:
                    break
            while True:
                correctness = input("Enter 0/1/2 string:  ")
                if len(correctness) != 5:
                    print("Sorry, 01010 length must be 5.")
                    continue
                else:
                    break
            self.word_to_functions(word=word, word_correctness=correctness)
            self.check_victory()
        replay = input("Press (y)es to play again, (n)o to exit")
        if replay == 'y':
            self.reset_file()
            self.run()


instructions = 'First input the word that you placed in the game. ' \
               '\nNext put a combination of zeros ones and twos based on the game outputs:' \
               '\n  0: incorrect letter' \
               '\n  1: correct letter incorrect place' \
               '\n  2: correct letter and place' \
               '\n' \
               '\nFor example if the underlying word is "carie" (unknown to the user) and they put the ' \
               'word "ceras" the game will show green-yellow-green-gray-gray, which the user should translate to ' \
               '"21200"' \
               '\n---------------------------------------------------------------------------------------------------' \
               '\n'

if __name__ == '__main__':
    input_file = open('sorted_words.json', "r", encoding='utf-8')
    word_list_string = input_file.read()
    five_word_list = eval(word_list_string)
    input_file.close()

    game = WordDecipher(five_word_list)
    print(instructions)
    game.run()
