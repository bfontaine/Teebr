# -*- coding: UTF-8 -*-

import re
import nltk
from unidecode import unidecode

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

# URLs + http:... at the end of truncated tweets
RE_HTTP = re.compile(r"\b(?:https?://\S+|https?:\.\.\.$)")

RE_SPACES = re.compile(r"\s+")

RE_HTML_ENTITY = re.compile(r"&[a-z]+;")

RE_RT = re.compile(r"^RT @\S+:?")
RE_END_HASHTAGS = re.compile(r"(?:#\S+\s*)+$")
RE_HASH = re.compile(r"#")
RE_MENTION = re.compile(r"@\S+")

SLANGS = [(re.compile(r"\b%s\b" % re.escape(s)),r) for s,r in (
    ("cuz", "because"),
    ("u r", "you are"),
    ("thx", "thanks"),

    # we use legit words instead of Twitter-specific language here
    ("DM", "private message"),
    ("RT", "write"),
    ("tweet", "message"),
)]

DEL_SLANGS = [re.compile(s, re.IGNORECASE) for s in (
    "asap",
    "lol",
    "rofl",
)]


def contains_emoji(text):
    """
    Test if some text contains emojis.
    """
    return RE_EMOJI.search(text) is not None


def unslangize(text):
    """
    Try to remove as many slang words as possible, replacing with their correct
    form.
    """
    for s in DEL_SLANGS:
        text = s.sub("", text)

    for reg, rep in SLANGS:
        text = reg.sub(rep, text)
    return text


def normalize_text(text):
    """
    Return a normalized version of a status, meant to be tokenized by NLTK for
    entity extraction.
    """
    # remove accents, emoji & co
    text = unidecode(unicode(text))

    # remove HTML stuff
    text = RE_HTML_ENTITY.sub("", text)

    # remove URLs
    text = RE_HTTP.sub("", text)

    # strip RT stuff:
    text = RE_RT.sub("", text)

    # strip hashtags at the end
    text = RE_END_HASHTAGS.sub("", text)

    # strip #'s
    text = RE_HASH.sub("", text)

    # strip mentions
    text = RE_MENTION.sub("", text)

    # replace slang
    text = unslangize(text)

    # compact spaces
    text = RE_SPACES.sub(" ", text).strip()

    return text

def extract_named_entities(text):
    """
    An attempt to extract named entities from a status' text
    """
    text = normalize_text(text)

    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    return [word for word, tag in tagged if tag.startswith("NN")]
