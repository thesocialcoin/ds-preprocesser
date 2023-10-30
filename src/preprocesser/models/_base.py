import re
import string
from typing import Tuple, List, Dict, Counter, Optional
from collections import Counter
import unicodedata

from preprocesser.data import make_stopwords

UNICODES = (
    "\u0E00-\u0E7F\u0621-\u064A\u0660-\u0669\u0980-\u09FF"
    "\u0D80-\u0DFF\uA8E0–\uA8FF\u0900–\u097F\u1CD0–\u1CFF"
)


def removeNonAlphChar(text: str) -> str:
    """Removes non alpha charaters from the text

    Args:
        text (_type_)

    Returns:
        str:
    """
    cleaned_text = ""
    for character in text:
        cleaned_text += (character
                         if unicodedata.category(character)[0]
                         in "LZNM" else " ")
    clean_spaces = " ".join(cleaned_text.split())
    return clean_spaces


def removeTags(text: str,
               placeholder="TAG",
               use_placeholder=True) -> Tuple[str, Dict[str, List[str]]]:
    """Removes every occurence of a tag or hashtag in the text
    Args:
        text (str):

    Returns:
        Tuple[str, Dict[str, List[str]]]
    """

    pattern = r'#\w+'

    # Use re.findall to find all hashtags in the text
    tags = re.findall(pattern, text)
    for tag in tags:
        text = (text.replace(tag, placeholder)
                if use_placeholder else text.replace(tag, ""))
    return text, {"tags": tags}


def removeUnicode(text: str) -> str:
    """Removes unicode strings like "\u002c" printable such as \t \r and \n

    Args:
        text (str): The input text
    """
    text = re.sub(r"(\\u[0-9A-Fa-f]+)", r"", text)
    text = re.sub(
        r"&amp;", "&", text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    ).strip()
    return text


def removeUrls(text: str,
               placeholder="URL",
               use_placeholder=True) -> Tuple[str, Dict[str, List[str]]]:
    """change URL by special token

    Args:
        text (str): The input text
    """
    urls = re.findall(
        (
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]"
            "|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        ),
        text,
    )
    for url in urls:
        text = (text.replace(url, placeholder)
                if use_placeholder else text.replace(url, ""))
#    while re.search(r"(URL)(.*)\1", text):
#        text = re.sub(r"(URL)(.*)\1", r"\1\2", text).strip()
    return text, {"urls": urls}


def removeHtMentionsSuccessions(text: str) -> Tuple[str, Dict[str, Optional[str]]]:
    """Remove #s and @s that are at the beginning or at the end of a tweet

    Args:
        text (str): The input text
    """
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


def toLower(text: str) -> str:
    """_summary_

    Args:
        text (str)

    Returns:
        str:

    Example:
        Input:
            @GoldingBF Giorgia is halting the migrant boats. Stemming the tide.
            Give her time to start the deportations.
            She has to prove Fratelli d'Italia can govern Italy.

        Output:
            @goldingbf giorgia is halting the migrant boats. stemming the tide.
            give her time to start the deportations. she has to prove fratelli
            d'italia can govern italy.
    """
    return text.lower()


def replaceAtUser(text: str,
                  placeholder="atUser",
                  use_placeholder=False) -> Tuple[str, Dict[str, List[str]]]:
    """Replaces "@user" with "atUser"

    Args:
        text (str): The input text
    """
    users = re.findall(r"@[\w+" + UNICODES + "]+", text)
    for user in users:
        text = (text.replace(user, placeholder)
                if use_placeholder else text.replace(user, ""))
    return text, {"users": users}


def removeHashtagInFrontOfWord(text: str) -> Tuple[str, Dict[str, List[str]]]:
    """Removes hastag in front of a word

    Args:
        text (str): The input text
    """
    hts = re.findall(r"#[\w+" + UNICODES + "]+", text)
    for ht in hts:
        text = text.replace(ht, ht[1:])
    return text, {"#s": hts}


def replaceMultiExclamationMark(text: str) -> Tuple[str, Dict[str, int]]:
    """Replaces repetitions of exlamation marks

    Args:
        text (str): The input text
    """
    exclams = re.findall(r"(\!)\1+", text)
    text = re.sub(r"(\!)\1+", r"!", text)
    return text, {"exclams": len(exclams)}


def replaceMultiQuestionMark(text: str) -> Tuple[str, Dict[str, int]]:
    """Replaces repetitions of question marks

    Args:
        text (str): The input text
    """
    questions = re.findall(r"(\?)\1+", text)
    text = re.sub(r"(\?)\1+", r"?", text)
    return text, {"questions": len(questions)}


def replaceMultiStopMark(text: str) -> Tuple[str, Dict[str, int]]:
    """Replaces repetitions of stop marks

    Args:
        text (str): The input text
    """
    stops = re.findall(r"(\.)\1+", text)
    text = re.sub(r"(\.)\1+", r".", text)
    return text, {"stops": len(stops)}


def replaceElongated(text: str) -> Tuple[str, Dict[str, int]]:
    """
    Replaces an elongated word with its
    basic form if it contains >2 repeated letters

    Args:
        text (str): The input text
    """
    quantifiers = '{2,}'
    pattern = fr"([a-zA-Z{UNICODES}]+)\1{quantifiers}"

    elongateds = re.findall(pattern, text)
    for _ in elongateds:
        text = re.sub(pattern, r"\1", text)

    return text, {"elongateds": len(elongateds)}


def removeEmojis(text: str) -> Tuple[str, Dict[str, List[str]]]:
    """
    Replaces emojis in the input text with a placeholder

    Args:
        text (str): The input text

    Returns:
        tuple: A tuple containing two elements:
            - str: The modified text with the placeholder EMOJI instead of the emojis.
            - dict: A dictionary with the key "emojis" mapping to a list of emojis retrieved from the text.
    """

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


def removeNumbers(text: str,
                  use_placeholder=False) -> Tuple[str, Dict[str, List[str]]]:
    """
    Replaces numbers (dates, prices, years and other numbers) in the input
    text with placeholders.

    Args:
        text (str): The input text.
        use_placeholder (bool): Set identifiers otherwise uses empty string

    Returns:
        tuple: A tuple containing two elements:
            - str: The modified text with placeholders instead of numbers.
            - dict: A dictionary with keys "dates," "years," "prices," and
            "other" mapping to lists of
              corresponding patterns found in the text.
    """

    pattern = r'\d{1,4}[-/ ]\d{1,4}[-/ ]\d{2,4}|(?:\d{1,2}[-/ ])?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/ ]\d{1,4}'

    dates = re.findall(pattern, text, re.IGNORECASE)

    for date in dates:
        text = text.replace(date, "DATEMENTION" if use_placeholder else "")
    prices = re.findall(
        r"""(?:[$€¥£₩]\s*(?:\d+[\. ,])?\d+(?:[, \.]\d+)?
        |(?:\d+[\. ,])?\d+(?:[, \.]\d+)?\s*[$€¥£₩])""",
        text,
    )
    for price in prices:
        text = text.replace(price, "PRICEMENTION" if use_placeholder else "")
    years = re.findall(r"[\d]{4}", text)

    for year in years:
        text = text.replace(year, "YYYY" if use_placeholder else "")

    numbers = re.findall(r"\b\d+\b", text)
    for number in numbers:
        text = text.replace(number, "NUM" if use_placeholder else "")

    return text, {
        "dates": dates,
        "years": years,
        "prices": prices,
        "other": numbers
        }


def removeStopWords(text: str, lang: str) -> Tuple[str, Dict[str, Counter]]:
    """
    Removes stopwords from the input text based on the specified language

    Args:
        text (str): The input text
        lang (str): The language code used to pick the stopwords list

    Input:
       text: "the sun shines"
       lang: "en"

    Output:
        "sun shines"

    Returns:
        tuple: A tuple containing two elements:
            - str: The modified text without stopwords.
            - dict: A dictionary with the key "stopwords" mapping to a Counter
            containing the retrieved stopwords and their counts.
    """

    stopwords = make_stopwords(lang)

    filtered_tokens = [token for token in text.split()
                       if not token.lower() in stopwords]

    found_stopwords = [token for token in text.split()
                       if token.lower() in stopwords]

    counts = Counter(found_stopwords)

    cleaned_text = ' '.join(filtered_tokens)

    return cleaned_text, {'stopwords': dict(counts)}


def removePunctuation(text: str) -> Tuple[str, Dict[str, List[str]]]:
    """
    Removes punctuation from the input text

    Args:
        text (str)

    Input:
       ""
    Output:
        ""

    Returns:
        tuple: A tuple containing two elements:
            - str: The modified text without punctuation.
            - dict: A dictionary with the key "punctuation" mapping to a list
            of the punctuation signs extracted from the text.
    """
    pattern = f'[{string.punctuation}¡¿]+'

    punctuation = re.findall(pattern, text)
    for _ in punctuation:
        text = re.sub(pattern, r" ", text)

    return text, {"punctuation": punctuation}


def removeMultiWhiteSpace(text: str) -> str:
    """
    Eliminate duplicate white spaces, e.g:

    Input:
       "  Hello World! ;) .  "
    Output:
        " Hello World! ;) . hola "

    Args:
        text (str)

    Returns:
        str
    """
    return re.sub(r"\s\s+", " ", text)
