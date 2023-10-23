import re
import string
from collections import Counter

from preprocesser.data import make_stopwords

UNICODES = (
    "\u0E00-\u0E7F\u0621-\u064A\u0660-\u0669\u0980-\u09FF"
    "\u0D80-\u0DFF\uA8E0–\uA8FF\u0900–\u097F\u1CD0–\u1CFF"
)


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


def tolower(text: str) -> str:
    return text.lower()


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
    """
    Replaces an elongated word with its
    basic form if it contains >2 repeated letters
    """
    quantifiers = '{2,}'
    pattern = fr"([a-zA-Z{UNICODES}]+)\1{quantifiers}"

    elongateds = re.findall(pattern, text)
    for _ in elongateds:
        text = re.sub(pattern, r"\1", text)

    return text, {"elongateds": len(elongateds)}


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


def removeStopWords(text, lang):

    stopwords = make_stopwords(lang)

    filtered_tokens = [token for token in text.split()
                       if not token.lower() in stopwords]

    found_stopwords = [token for token in text.split()
                       if token.lower() in stopwords]

    counts = Counter(found_stopwords)

    cleaned_text = ' '.join(filtered_tokens)

    return cleaned_text, {'stopwords': dict(counts)}

def removePunctuation(text):
    pattern = f'[{string.punctuation}¡¿]+'

    punctuation = re.findall(pattern, text)
    for _ in punctuation:
        text = re.sub(pattern, r" ", text)

    return text, {"punctuation": punctuation}
