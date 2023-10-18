import re
import json

import pkg_resources
from collections import Counter

from numpy.typing import ArrayLike

from typing import Optional

import pandas as pd
import multiprocessing as mp
import time

UNICODES = (
    "\u0E00-\u0E7F\u0621-\u064A\u0660-\u0669\u0980-\u09FF"
    "\u0D80-\u0DFF\uA8E0–\uA8FF\u0900–\u097F\u1CD0–\u1CFF"
)

SUPPORTED_LANGUAGES = ["en"]


class PreProcesser:

    def __init__(self,
                 remove_unicode=True,
                 remove_urls=True,
                 remove_mentions=True,
                 remove_hashtags=True,
                 remove_multiple_exclamations=True,
                 remove_multiple_questions=True,
                 remove_multiple_periods=True,
                 remove_elongated=True,
                 remove_emojis=True,
                 remove_numbers=True,
                 to_lowercase=True,
                 replace_at_user=True
                 ):

        self.remove_unicode = remove_unicode
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_multiple_exclamations = remove_multiple_exclamations
        self.remove_multiple_questions = remove_multiple_questions
        self.remove_multiple_periods = remove_multiple_periods
        self.remove_elongated = remove_elongated
        self.to_lowercase = to_lowercase
        self.remove_emojis = remove_emojis
        self.remove_numbers = remove_numbers
        self.replace_at_user = replace_at_user

    def __call__(self, text):
        """
        Objective: consolidations of all pre-processing

        Inputs:
                - text, str: the text to pre_process
        Outputs:
                - features, dict: the dictionary with raw text,
                pped text and all features extracted
        """
        features = {"raw_text": text}

        if self.remove_unicode:
            text = removeUnicode(text)

        text, urls = removeUrls(text) if self.remove_urls else (text, {})

        text, ht_mts = (removeHtMentionsSuccessions(text)
                        if self.remove_mentions else (text, {}))

        text, users = (replaceAtUser(text)
                       if self.replace_at_user else (text, {}))

        text, hts = (removeHashtagInFrontOfWord(text)
                     if self.remove_hashtags else (text, {}))

        text, exclams = (replaceMultiExclamationMark(text)
                         if self.remove_multiple_exclamations else (text, 0))

        text, questions = (replaceMultiQuestionMark(text)
                           if self.remove_multiple_questions else (text, 0))

        text, stops = (replaceMultiStopMark(text)
                       if self.remove_multiple_periods else (text, 0))

        text, elongated = (replaceElongated(text)
                           if self.remove_elongated else (text, 0))

        text, capitalized = (replaceCapitalized(text)
                             if self.to_lowercase else (text, {}))

        text, emojis = removeEmojis(text) if self.remove_emojis else (text, {})

        text, numbers = (removeNumbers(text)
                         if self.remove_numbers else (text, {}))

        features = {
            **features,
            **urls,
            **{"successions": ht_mts},
            **users,
            **hts,
            **emojis,
            **exclams,
            **questions,
            **stops,
            **elongated,
            **capitalized,
            **{"numbers": numbers},
        }
        features["text"] = text

        return features


class EN_PreProcesser(PreProcesser):
    """English preprocessor"""

    def __call__(self, text):
        return super().__call__(text)


def preprocesser_factory(lang: str):
    assert lang in SUPPORTED_LANGUAGES

    if lang == "en":
        return EN_PreProcesser
    # ...


def removeUnicode(text):
    """Removes unicode strings like "\u002c" printable such as \t \r and \n"""
    text = re.sub(r"(\\u[0-9A-Fa-f]+)", r"", text)
    text = re.sub(
        r"&amp;", "&", text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    ).strip()
    return text


def removeUrls(text):
    """change URL by special token"""
    urls = re.findall(
        (
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]"
            "|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        ),
        text,
    )
    for url in urls:
        text = text.replace(url, "URL")
    while re.search(r"(URL)(.*)\1", text):
        text = re.sub(r"(URL)(.*)\1", r"\1\2", text).strip()
    return text, {"urls": urls}


def removeHtMentionsSuccessions(text):
    """Remove #s and @s that are at the beginning or at the end of a tweet"""
    ht_mts = {}

    ht_mts["begin"] = re.search(r"^(URL\s*)*([@#][\w+" + UNICODES + r"]+\s){1,}", text)

    if ht_mts["begin"]:
        begin = ht_mts.get("begin")
        if "URL" in text[begin.start() : begin.end()]:
            text = "URL " + text[begin.end() :]
        else:
            text = text[begin.end() :]
        ht_mts["begin"] = begin.group()

    ht_mts["end"] = re.search(r"(\s[@#][\w+" + UNICODES + r"]+){1,}(URL\s*)*$", text)

    if ht_mts["end"]:
        if "URL" in text[ht_mts.get("end").start() : ht_mts.get("end").end()]:
            text = text[: ht_mts.get("end").start()] + " URL"
        else:
            text = text[: ht_mts.get("end").start()]
        ht_mts["end"] = ht_mts.get("end").group()

    return text, ht_mts


def replaceAtUser(text):
    """Replaces "@user" with "atUser" """
    users = re.findall(r"@[\w+" + UNICODES + "]+", text)
    for user in users:
        text = text.replace(user, "atUser")
    return text, {"users": users}


def removeHashtagInFrontOfWord(text):
    """Removes hastag in front of a word"""
    hts = re.findall(r"#[\w+" + UNICODES + "]+", text)
    for ht in hts:
        text = text.replace(ht, ht[1:])
    return text, {"#s": hts}


def replaceMultiExclamationMark(text):
    """Replaces repetitions of exlamation marks"""
    exclams = re.findall(r"(\!)\1+", text)
    text = re.sub(r"(\!)\1+", r"!", text)
    return text, {"exclams": len(exclams)}


def replaceMultiQuestionMark(text):
    """Replaces repetitions of question marks"""
    questions = re.findall(r"(\?)\1+", text)
    text = re.sub(r"(\?)\1+", r"?", text)
    return text, {"questions": len(questions)}


def replaceMultiStopMark(text):
    """Replaces repetitions of stop marks"""
    stops = re.findall(r"(\.)\1+", text)
    text = re.sub(r"(\.)\1+", r".", text)
    return text, {"stops": len(stops)}


def replaceElongated(text):
    """Replaces an elongated word with its basic form with >2 --> 2 letters"""
    elongateds = re.findall(r"([a-zA-Z])\1{2,}", text)
    text = re.sub(r"([a-zA-Z" + UNICODES + "]+)\1{2,}", r"\1\1", text)
    return text, {"elongateds": len(elongateds)}


def replaceCapitalized(text):
    capitalized = re.findall(r"\b[A-Z0-9]{3,}\b", text)
    for cap in capitalized:
        if cap != "URL":
            text = text.replace(cap, cap.lower())
    return text, {"capitalized": capitalized}


def removeEmojis(text):

    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "]+"
    )

    emojis = emoji_pattern.findall(text)
    for emoji in emojis:
        text = text.replace(emoji, " EMOJI ")
    return text, {"emojis": emojis}


def removeNumbers(text):

    dates = re.findall(
        r"""(?:[\d]{1,2}[/-][\d]{1,2}[/-]
        (?:[\d]{4}|[\d]{2})|[\d]{1,2} [a-zA-Z]{3,} [\d]{4})""",
        text,
    )
    for date in dates:
        text = text.replace(date, "DATEMENTION")
    prices = re.findall(
        r"""(?:[$€¥£₩]\s*(?:\d+[\. ,])?\d+(?:[, \.]\d+)?
        |(?:\d+[\. ,])?\d+(?:[, \.]\d+)?\s*[$€¥£₩])""",
        text,
    )
    for price in prices:
        text = text.replace(price, "PRICEMENTION")
    years = re.findall(r"[\d]{4}", text)

    for year in years:
        text = text.replace(year, "YYYY")

    numbers = re.findall(r"\b\d+\b", text)
    for number in numbers:
        text = text.replace(number, "NUM")

    return text, {
        "dates": dates,
        "years": years,
        "prices": prices,
        "other": numbers
        }

def removeStopwords(text, lang):

    data_path = pkg_resources.resource_filename('cbpreprocessing', 'data/stop-words/languages.json')

    with open(data_path) as f:
        all_langs = json.load(f)

    stopwords_file_path = pkg_resources.resource_filename('cbpreprocessing', f'data/stop-words/{all_langs[lang]}.txt')

    with open(stopwords_file_path) as f:
        stopwords= f.readlines()

    stopwords = [line.strip() for line in stopwords]

    filtered_tokens = [token for token in text.split() if not token.lower() in stopwords]

    found_stopwords = [token for token in text.split() if token.lower() in stopwords]
    counts = Counter(found_stopwords)

    cleaned_text = ' '.join(filtered_tokens)

    return cleaned_text, {'stopwords': dict(counts)}


def sequential_preprocessing(p: PreProcesser,
                             text_set: ArrayLike,
                             verbose=False) -> ArrayLike:
    """
    Preprocess a list of texts in sequential

    :p
        - Preprocesser class
    :text_text
        - Set of text that need to be mapped
    """

    if verbose:
        print("Total records of the dataset", len(text_set))

    df = pd.DataFrame({'text': text_set})
    t1 = time.time()
    df['text'] = df['text'].apply(p)
    t2 = time.time()

    if verbose:
        print("Time consuming Sequential Processing to process " +
              "the Dataset {0:.2f}s".format(round(t2-t1, 2)))
    return df['text'].values


def parallel_preprocessing(p: PreProcesser,
                           text_set: ArrayLike,
                           njobs: Optional[int] = None,
                           verbose=False) -> ArrayLike:
    """
    Preprocess a list of texts in parallel.
    The performance is evident when you deal with
    a big dataset of text.

    :p
        - Preprocesser class
    :text_text
        - Set of text that need to be mapped
    :njobs
        - Number of threds used. If is set to None,
        it uses the available number of threds.
    """

    if verbose:
        print("Total records of the dataset", len(text_set))

    df = pd.DataFrame({'text': text_set})
    processes = njobs if njobs else (mp.cpu_count() - 1
                                     if mp.cpu_count() > 1
                                     else mp.cpu_count())
    t1 = time.time()
    with mp.Pool(processes=processes) as pool:
        df['text'] = pool.map(p, text_set)
    t2 = time.time()

    if verbose:
        print("Time consuming Parallel Processing to process " +
              "the Dataset {0:.2f}s".format(round(t2-t1, 2)))
    return df['text'].values

