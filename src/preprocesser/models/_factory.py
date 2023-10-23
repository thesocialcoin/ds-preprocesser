from typing import Optional

from . import (EN_PreProcesser,
               ES_PreProcesser,
               PreProcesser)

SUPPORTED_LANGUAGES = ["en", "es"]


def preprocesser_factory(lang: Optional[str]):

    if lang is None:
        return PreProcesser

    assert lang in SUPPORTED_LANGUAGES

    if lang == "en":
        return EN_PreProcesser
    elif lang == "es":
        return ES_PreProcesser

    return PreProcesser
