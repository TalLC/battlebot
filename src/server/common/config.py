from pathlib import Path

DATETIME_STR_FORMAT = '%d/%m/%Y %H:%M:%S'

WORDS_ADJECTIVES_DICTIONARY_PATH = Path('conf', 'dictionaries', 'english-adjectives.txt').read_text()
WORDS_ADJECTIVES_LIST = WORDS_ADJECTIVES_DICTIONARY_PATH.replace('\r\n', '\n').split('\n')

WORDS_GERUNDS_DICTIONARY_PATH = Path('conf', 'dictionaries', 'english-gerunds.txt').read_text()
WORDS_GERUNDS_LIST = WORDS_GERUNDS_DICTIONARY_PATH.replace('\r\n', '\n').split('\n')

WORDS_NOUNS_DICTIONARY_PATH = Path('conf', 'dictionaries', 'english-nouns.txt').read_text()
WORDS_NOUNS_LIST = WORDS_NOUNS_DICTIONARY_PATH.replace('\r\n', '\n').split('\n')
