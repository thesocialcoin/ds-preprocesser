import json
from os.path import join
import pkg_resources

from preprocesser import __name__


def make_stopwords(lang: str) -> set[str]:

    stop_words_uri = join('data', 'stop-words')
    data_path = pkg_resources \
        .resource_filename(__name__, f"{stop_words_uri}/languages.json")

    with open(data_path) as f:
        all_langs = json.load(f)

    stopwords_file_path = pkg_resources \
        .resource_filename(__name__, f'{stop_words_uri}/{all_langs[lang]}.txt')

    with open(stopwords_file_path) as f:
        stopwords = f.readlines()

    stopwords = set([line.strip() for line in stopwords])

    return stopwords
