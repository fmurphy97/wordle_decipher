from wordle_decipher.decipher_game import *
from wordle_decipher.game import *
from wordle_decipher.initial_word import *
from wordle_decipher.word_cleanup import create_input_list
from wordle_decipher.config import WORD_SIZE, LANGUAGE
import sys
import os
import pandas as pd



_INITIAL_WORD = get_best_initial_word()

def run_automatically(game, decipher_game):
    game.reset_game()
    decipher_game.reset_word_decipher()

    word = _INITIAL_WORD
    print(f'Chosen word:{word}')
    result = game.make_output(word)
    game.check_victory(result)
    correctness = "".join([str(x) for x in result])
    decipher_game.filter_possible_results(word=word, word_correctness=correctness)

    while not game.complete:
        word = decipher_game.filtered_list[0]
        if not game.complete:
            print(f'Chosen word:{decipher_game.filtered_list[0]}')
        result = game.make_output(word)
        game.check_victory(result)
        correctness = "".join([str(x) for x in result])
        decipher_game.filter_possible_results(word=word, word_correctness=correctness)

    return game.attempt, game.won


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def avg(input_list):
    return sum(input_list) / len(input_list)


if __name__ == '__main__':
    block_print()
    dictionary_word_list = create_input_list(word_length=WORD_SIZE, language=LANGUAGE)
    game = WordGame(dictionary_word_list, word_length=WORD_SIZE)
    decipher = WordDecipher(dictionary_word_list, word_length=WORD_SIZE)
    attempts = []
    wins = []
    iterations = 1000
    for i in range(iterations):
        attempt, won = run_automatically(game, decipher)
        attempts.append(attempt)
        if won:
            wins.append(1)
        else:
            wins.append(0)

    enable_print()

    print(f'Code was run for {iterations} iterations')
    print(f'Average attempts: {avg(attempts)}')
    print(f'Wins: {round(avg(wins)*100,2)}%')
    print('----------------------------------------------------------------------------------------------')
    df = pd.DataFrame.from_dict(dict(Counter(attempts)), orient='index', columns=['count']).sort_index()
    df.index.name = 'attempts'
    new_row = pd.Series(data={'count': (len(wins)-sum(wins))}, name='losses')
    df = df.append(new_row, ignore_index=False)
    df['%'] = (df['count'] / df['count'].sum()) * 100
    print(df)