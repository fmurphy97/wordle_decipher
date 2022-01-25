import pandas as pd
import pathlib
from config import WORD_SIZE, LANGUAGE, special_characters_all_languages, characters_all_languages


def create_input_list(word_length=WORD_SIZE, language=LANGUAGE):
    path = pathlib.Path(__file__).parent.resolve().joinpath('data_files', f'{language}_words.csv')
    df = pd.read_csv(path, header=0, dtype=str)
    characters = characters_all_languages[language]
    special_characters = special_characters_all_languages[language]
    dictionary_word_list = []
    for word in list(df['word']):
        if len(str(word)) == word_length:
            add_word = True
            letters = list(str(word))
            for lno, letter in enumerate(letters):
                if letter not in characters:
                    add_word = False
                    break
                if letter in special_characters.keys():
                    letters[lno] = special_characters[letter]
            if add_word:
                word = "".join(letters)
                dictionary_word_list.append(word)

    return list(dict.fromkeys(dictionary_word_list))
