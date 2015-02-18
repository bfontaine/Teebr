# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from collections import defaultdict

from .textutils import contains_emoji, extract_named_entities

LANGUAGES = ('en',) # 'fr')

SOURCE_TYPES = {
    "source_mobile": [
        "Echofon",
        "Mobile Web (M2)",
        "Mobile Web (M5)",
        "Mobile Web",
        "Samsung Mobile",
        "Twitter for Android",
        "Twitter for BlackBerry®",
        "Twitter for Windows Phone",
        "Twitter for iPhone",
        "Twitterrific",
        "iOS",
        "uberSocial for Android",
    ],
    "source_tablet": [
        "Twitter for Android Tablets",
        "Twitter for iPad",
    ],
    "source_desktop": [
        "TweetDeck",
        "Twitter Web Client",
        "Twitter for Mac",
        "OS X",
    ],
    # automated publication tools + bot-like tweets
    "source_autopub": [
        "Buffer",
        "Hootsuite",
        "IFTTT",
        "JustUnfollow",
        "RoundTeam",
        "TweetAdder v4",
        "fllwrs",
        "twittbot.net",
    ],
    "source_social": [
        "Ask.fm",
        "Facebook",
        "Foursquare",
        "Instagram",
        "LinkedIn",
        "Path",
        "Pinterest",
        "Reddit RSS",
        "Vine - Make a Scene",
        "Vine for Android",
    ],
    "source_news": [
        "Nachrichten News",
    ],

    "source_other": [],
}

URL_TYPES = {
    "url_social": [
        "fb.me",
        "path.com",
    ],
    "url_social_media": [
        "vine.co",
        "instagram.com",
    ],
    "url_product": [
        "amzn.to",
    ],
    "url_video": [
        "youtu.be",
    ],
}


def filter_status(st):
    """
    Check if we should include a status as returned by the Streaming API in our
    DB. It'll return ``False`` if it should be rejected.
    """
    # keep only some languages
    if st.lang not in LANGUAGES:
        return False

    # remove replies
    if st.in_reply_to_screen_name:
        return False

    # remove manual RTs
    if st.text.startswith("RT @"):
        return False

    # ok
    return True


class FeaturesDict(defaultdict):
    def __init__(self, st):
        super(FeaturesDict, self).__init__(float)
        self._st = st

    def compute_features(self):
        """
        Compute all features for this tweet
        """
        self._set_source_type()

        self["sg_geolocalized"] = self._st.geo is not None
        self["sg_lang_%s" % self._st.lang] = 1
        self["sg_contributors"] = self._st.contributors is not None
        self["sg_emojis"] = contains_emoji(self._st.text)
        self["sg_nsfw"] = self._st.possibly_sensitive

        self["names"] = ",".join(extract_named_entities(self._st.text))

        for key in ("urls", "hashtags", "user_mentions", "trends", "symbols"):
            self["sg_%s" % key] = int(bool(self._st.entities["urls"]))


    def _set_source_type(self):
        """
        Feature: source type
        Keys: source_mobile, source_desktop, source_autopub, source_social,
            source_tablet, source_other, ... (see SOURCE_TYPES)
        Values: [0, 1]
        """
        text = self._st.source.strip()

        for s,vs in SOURCE_TYPES.items():
            if text in vs:
                self["sg_%s" % s] = 1
                return

        ltext = text.lower()
        for brand in ("android", "iphone", "blackberry", "windows phone"):
            if ltext.endswith(" for %s" % brand):
                self["sg_source_mobile"] = 1
                return

        self["sg_source_others"] = 1


def compute_features(status):
    f = FeaturesDict(status)
    f.compute_features()
    return f
