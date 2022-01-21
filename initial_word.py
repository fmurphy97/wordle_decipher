from collections import Counter
from itertools import chain
import operator

input_file = open('sorted_words.json', "r", encoding='utf-8')
word_list_string = input_file.read()
five_word_list = eval(word_list_string)
input_file.close()

WORD_LENGTH=5
LETTER_COUNTER = Counter(chain.from_iterable(five_word_list))

LETTER_FREQUENCY = {
    character: value / sum(LETTER_COUNTER.values())
    for character, value in LETTER_COUNTER.items()
}

for letter in {'a','e','i','o','u'}:
    LETTER_FREQUENCY[letter]  = 0.02

def calculate_word_commonality(word):
    score = 0.0
    for char in word:
        score += LETTER_FREQUENCY[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)

def sort_by_word_commonality(words):
    sort_by = operator.itemgetter(1)
    return sorted(
        [(word, calculate_word_commonality(word)) for word in words],
        key=sort_by,
        reverse=True,
    )
