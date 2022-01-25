available_languages = ['english', 'spanish', 'french']

WORD_SIZE = 5
LANGUAGE = 'english'

# This is just to check the input is correct
LANGUAGE = available_languages[available_languages.index(LANGUAGE)]

# The game does not accept special characters,
# place them in the dictionary according to the replacement the game should use
special_characters_all_languages = {'spanish': {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'},
                                    'english': {},
                                    'french': {'à': 'a', 'â': 'a', 'ã': 'a', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                                               'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'ù': 'u', 'û': 'u', 'ü': 'u'}
                                    }

# The words in the datasets may contain unwanted characters, remove the ones that do not belong to the language
characters_all_languages = {'spanish': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o',
                                        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                        'á', 'é', 'í', 'ó', 'ú', 'ü'],
                            'english': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                                        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
                            'french': {"'", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                                       'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'à', 'â', 'ã', 'ç', 'è',
                                       'é', 'ê', 'ë', 'î', 'ï', 'ô', 'ö', 'ù', 'û', 'ü'}
                            }
