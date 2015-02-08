# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import re

# codes from http://stackoverflow.com/a/12824140/735926
RE_EMOJI = re.compile(
        "["
            r"\U00002600-\U000026FF"  # Misc Symbols
            r"\U00002700-\U000027BF"  # Dingbats
        #   TODO:
        #   r"\U0001F300-\U0001F5FF"  # Misc Symbols & Pictographs
        #   r"\U0001F600-\U0001F64F"  # Emoticons
        #   r"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "]"
, re.UNICODE)

def contains_emoji(text):
    """
    Test if some text contains emojis.
    """
    return RE_EMOJI.search(text) is not None
