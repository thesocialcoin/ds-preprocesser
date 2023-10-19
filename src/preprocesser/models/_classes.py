from typing import Optional, Any, Dict

from . import (removeEmojis,
               removeHashtagInFrontOfWord,
               removeHtMentionsSuccessions,
               removeNumbers,
               removeStopWords,
               removeUnicode,
               removeUrls,
               replaceMultiStopMark,
               replaceAtUser,
               replaceCapitalized,
               replaceElongated,
               replaceMultiExclamationMark,
               replaceMultiQuestionMark)


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
                 replace_at_user=True,
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

    def __init__(self, args: Optional[Dict[str, Any]] = None):

        args_ = {
            "remove_stopwords": True,
            **(args or {})
        }

        self.remove_stopwords = args_["remove_stopwords"]

        if "remove_stopwords" in args_:
            del args_["remove_stopwords"]

        super().__init__(**args_)

    def __call__(self, text):
        base_preprocesser = super().__call__(text)
        text = base_preprocesser["text"]

        text, stopwords = (removeStopWords(text, "en")
                           if self.remove_stopwords else (text, {}))
        features = {
            **base_preprocesser,
            **stopwords
        }
        features["text"] = text
        return features


class ES_PreProcesser(PreProcesser):
    """Espanish preprocessor"""

    def __init__(self, args: Optional[Dict[str, Any]] = None):

        args_ = {
            "remove_stopwords": True,
            **(args or {})
        }

        self.remove_stopwords = args_["remove_stopwords"]

        if "remove_stopwords" in args_:
            del args_["remove_stopwords"]

        super().__init__(**args_)

    def __call__(self, text):
        base_preprocesser = super().__call__(text)
        text = base_preprocesser["text"]

        text, stopwords = (removeStopWords(text, "es")
                           if self.remove_stopwords else (text, {}))
        features = {
            **base_preprocesser,
            **stopwords
        }
        features["text"] = text
        return features
