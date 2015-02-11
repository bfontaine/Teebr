# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from .textutils import contains_emoji

LANGUAGES = ('en', 'fr')

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

    # ok
    return True


class ProcessedStatus(object):
    """
    A wrapper for a status with a ``compute_features`` method.
    """

    def __init__(self, st):
        self._st = st
        self.features = {}


    def compute_features(self):
        """
        Compute all features for this tweet
        """
        self.set_source_type()
        self.set_geo()
        self.set_lang()
        self.set_emojis()
        self.set_entities()
        self.set_contributors()


    def register_features(self, names):
        """
        Quick shortcut to add a list of features, each one being a string which
        will be added as a feature with the value ``0``.
        """
        for n in names:
            self.features[n] = 0


    def set_source_type(self):
        """
        Feature: source type
        Keys: source_mobile, source_desktop, source_autopub, source_social,
            source_tablet, source_other, ... (see SOURCE_TYPES)
        Values: [0, 1]
        """
        self.register_features(SOURCE_TYPES.keys())
        text = self._st.source.strip()

        for s,vs in SOURCE_TYPES.items():
            if text in vs:
                self.features[s] = 1
                return

        ltext = text.lower()
        for brand in ("android", "iphone", "blackberry", "windows phone"):
            if ltext.endswith(" for %s" % brand):
                self.features["source_mobile"] = 1
                return

        self.features["source_others"] = 1


    def set_geo(self):
        """
        Feature: geolocalized
        Keys: geolocalized
        Values: [0, 1]
        """
        self.features["geolocalized"] = self._st.geo is not None


    def set_lang(self):
        """
        Feature: language
        Keys: lang_en, lang_fr
        Values: [0, 1]
        """
        self.register_features(["lang_%s" % l for l in LANGUAGES])
        self.features["lang_%s" % self._st.lang] = 1


    def set_emojis(self):
        """
        Feature: emojis
        Keys: emojis
        Values: [0, 1]
        """
        self.features["emojis"] = contains_emoji(self.text)


    def set_entities(self):
        for key in ("urls", "hashtags", "mentions"):
            self.features[key] = int(bool(self._st.entities["urls"]))


    def set_contributors(self):
        self.features["contributors"] = self._st.contributors is not None
