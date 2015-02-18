# -*- coding: UTF-8 -*-

import re
from unidecode import unidecode

from .textsets import stopwords_re, punctuation_re, sounds_re

# codes from http://stackoverflow.com/a/12824140/735926
RE_EMOJI = re.compile(
        "["
            r"\U00002600-\U000026FF"  # Misc Symbols
            r"\U00002700-\U000027BF"  # Dingbats
            r"\U0001F300-\U0001F5FF"  # Misc Symbols & Pictographs
            r"\U0001F600-\U0001F64F"  # Emoticons
            r"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "]"
, re.UNICODE)

RE_HTTP = re.compile(r"\bhttps?://\S+")

RE_SPACES = re.compile(r"\s+")

RE_HTML_ENTITY = re.compile(r"&[a-z]+;")

def contains_emoji(text):
    """
    Test if some text contains emojis.
    """
    return RE_EMOJI.search(text) is not None


def normalize_text(text):
    """
    Return a normalized version of status, using aggressive replacements and
    other modifications.
    """
    # remove accents, emoji & co
    text = unidecode(unicode(text))

    # remove HTML stuff
    text = RE_HTML_ENTITY.sub("", text)

    # remove URLs
    text = RE_HTTP.sub("", text)

    # remove useless words/expressions
    text = stopwords_re.sub("", text)
    text = sounds_re.sub("", text)

    # remove punctuation
    text = punctuation_re.sub(" ", text)

    # compact spaces
    text = RE_SPACES.sub(" ", text).strip()

    return text
