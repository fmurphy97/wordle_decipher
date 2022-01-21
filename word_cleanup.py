import pandas as pd
import json
import pathlib

path = pathlib.Path(__file__).parent.resolve().joinpath('raw_data', 'palabras_por_frecuencia.csv')
df = pd.read_csv(path, header=0, dtype=str)
characters = 'qwertyuiopasdfghjklzxcvbnmáéíóúü'
special_characters = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
five_word_list = []
for word in list(df['words']):
    if len(str(word)) == 5:
        add_word = True
        letters = list(word)
        for lno, letter in enumerate(letters):
            if letter not in characters:
                add_word = False
                break
            if letter in special_characters.keys():
                letters[lno] = special_characters[letter]
        if add_word:
            word = "".join(letters)
            five_word_list.append(word)

print(len(five_word_list))
five_word_list = list(dict.fromkeys(five_word_list))
print(len(five_word_list))
json_object = json.dumps(five_word_list)
outfile = open("sorted_words.json", "w", encoding='utf-8')
outfile.write(json_object)
outfile.close()
