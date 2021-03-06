# -*- coding: UTF-8 -*-

import re
from unidecode import unidecode
from HTMLParser import HTMLParser

from textblob import TextBlob

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
RE_NUMBERS = re.compile("\d+")

RE_HTML_ENTITY = re.compile(r"&[a-z]+;")

RE_RT = re.compile(r"^RT @\S+:?")
RE_END_HASHTAGS = re.compile(r"(?:#\S+\s*)+$")
RE_HASH = re.compile(r"#")
RE_MENTION = re.compile(r"@\S+")

# some tweets contain lots of hashs, e.g.: ####### and this confuse the
# RE_END_HASHTAGS replacement that takes a lot of time. We add this one before
# to remove these repetitions
RE_HASHS = re.compile(r"##+")

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

# named entities we don't want to extract
NAMES_BLACKLIST = set([
    "(", ")", "[", "]", "+", "|", "%", "...", "~", "_", ":[",
    "The", "Of", "In", "", "n", "t", "\n", "m", "x", "N",
    "ll", "re", "ve", "pm",
])

htmlparser = HTMLParser()


def compile_OR_pattern(patterns, *args):
    s = "(?:%s)" % "|".join([re.escape(p) for p in patterns])
    return re.compile(s, *args)


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

    Note that on an Homebrewed Python on OS X the function might print warnings
    like: ::

        RuntimeWarning: Surrogate character u'\\udf05' will be ignored

    You can safely ignore them.
    """
    # remove accents, emoji & co
    text = unidecode(unicode(text))

    # remove HTML stuff
    text = htmlparser.unescape(text)

    # remove URLs
    text = RE_HTTP.sub("", text)

    # strip RT stuff:
    text = RE_RT.sub("", text)

    # strip hashtags at the end
    text = RE_HASHS.sub("", text)
    text = RE_END_HASHTAGS.sub("", text)

    # strip #'s
    text = RE_HASH.sub("", text)

    # strip mentions
    text = RE_MENTION.sub("", text)

    # replace slang
    text = unslangize(text)

    # remove numbers (this is very aggressive)
    text = RE_NUMBERS.sub("", text)

    # compact spaces
    text = RE_SPACES.sub(" ", text).strip()

    return text

def extract_named_entities(text):
    """
    An attempt to extract named entities from a status' text
    """
    text = normalize_text(text)

    blob = TextBlob(text)
    tagged = blob.tags

    words = [word.strip().replace(",", " ") for word, tag in tagged \
                if tag.startswith("NN")]
    return [word for word in words if word not in NAMES_BLACKLIST]


most_common_words = set([
    "amazon",
    "android",
    "app",
    "apple",
    "apps",
    "australia",
    "bbm",
    "blog",
    "california",
    "ceo",
    "change",
    "china",
    "company",
    "developer",
    "engadget",
    "entrepreneur",
    "everything",
    "facebook",
    "food",
    "fyi",
    "galaxy",
    "google",
    "green",
    "happy",
    "interview",
    "ios",
    "ipad",
    "iphone",
    "ipod",
    "itunes",
    "java",
    "life",
    "linux",
    "love",
    "macbook",
    "microsoft",
    "mobile",
    "music",
    "netflix",
    "nfl",
    "night",
    "nyt",
    "office",
    "people",
    "phone",
    "product",
    "programming",
    "python",
    "reuters",
    "review",
    "school",
    "seo",
    "social",
    "software",
    "someone",
    "startup",
    "startups",
    "store",
    "sxsw",
    "tech",
    "technology",
    "tesla",
    "thing",
    "touch",
    "tv",
    "twitter",
    "uk",
    "video",
    "watch",
    "web",
    "windows",
    "women",
    "work",
    "world",
    "youtube",
])
