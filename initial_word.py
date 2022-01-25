from collections import Counter
from itertools import chain
import operator
from word_cleanup import create_input_list
from config import WORD_SIZE, LANGUAGE

def calculate_word_commonality(word, LETTER_FREQUENCY, word_length=WORD_SIZE):
    score = 0.0
    for char in word:
        score += LETTER_FREQUENCY[char]
    return score / (word_length - len(set(word)) + 1)

def sort_by_word_commonality(words, LETTER_FREQUENCY, word_length=WORD_SIZE):
    sort_by = operator.itemgetter(1)
    return sorted(
        [(word, calculate_word_commonality(word, LETTER_FREQUENCY, word_length=word_length)) for word in words],
        key=sort_by,
        reverse=True,
    )

def get_best_initial_word(word_length=WORD_SIZE):
    dictionary_word_list = create_input_list(word_length=word_length, language=LANGUAGE)

    LETTER_COUNTER = Counter(chain.from_iterable(dictionary_word_list))

    LETTER_FREQUENCY = {
        character: value / sum(LETTER_COUNTER.values())
        for character, value in LETTER_COUNTER.items()
    }
    final_list = ([x[0] for x in sort_by_word_commonality(dictionary_word_list, LETTER_FREQUENCY,word_length=word_length )[:1000]])
    return final_list[0]

def get_best_initial_words_manually():
    dictionary_word_list = create_input_list(word_length=WORD_SIZE, language=LANGUAGE)

    LETTER_COUNTER = Counter(chain.from_iterable(dictionary_word_list))

    LETTER_FREQUENCY = {
        character: value / sum(LETTER_COUNTER.values())
        for character, value in LETTER_COUNTER.items()
    }
    final_list = ([x[0] for x in sort_by_word_commonality(dictionary_word_list, LETTER_FREQUENCY)[:1000]])
    print(final_list[:100])


if __name__ == '__main__':
    get_best_initial_words_manually()
    input("Press enter to exit")