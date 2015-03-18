# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

import re
from json import dumps
from collections import defaultdict

import bayes

from .log import mkLogger
from .text.utils import contains_emoji, extract_named_entities

logger = mkLogger("features")

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

# TODO we might be able to remove this now that we have a spam filter
APPS_BLACKLIST = set([
    # followers spam
    u"Unfollowers",
    u"JustUnfollow",
    u"fllwrs",
    u"..ignite.v.1.",
    u"Adi Sumardiyasa",
    u"Who Unfollowed Me",

    # tweets ranking
    u"001FM Top40 Tweets",

    # Games
    u"1Dreamboy 2 Game",
    u"1Dreamboy Version 2 Game",
    u"Airport City Mobile",
    u"The Tribez HD on iOS",

    # General news
    u"233Live Tweets",
    u"247newz",

    # Misc news
    u"ADVFN News Alert",
    u"APD Traffic Alerts",

    # Buzzfeed-like
    u"75325love",
    u"AlltheGoss",
    u"AllHealthSecrets.com",
    u"Amusing information",
    u"volkanc",
    u"awe.sm",

    # nsfw
    u"definebabecom",
    u"Cumagination Gay",
    u"Cumagination Lesbian",
    u"EscortGuidexXx",
    u"TweetAdder v",

    # Misc Spam
    u";sdklafjas",
    u"Acne-Treatments-and-Tips.com",
    u"AmazonRecommend",

    # Others
    u"Adcourier",
])

# some apps add numbers at the end, e.g. MySpam, MySpam1, MySpam2, etc
END_DIGITS = re.compile(r"\s*\d+$")

entity_keys = ("urls", "hashtags", "user_mentions", "trends", "symbols", "media")

storage = bayes.Storage("bayes.dat", 10)
storage.load()
spamFilter = bayes.Bayes(storage).is_spam


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

    # remove RTs
    if getattr(st, 'retweeted_status', False):
        return False

    # remove suspicious apps
    if not st.source or not st.source_url:
        return False

    # remove spam apps
    if END_DIGITS.sub("", st.source) in APPS_BLACKLIST:
        return False

    # remove manual RTs
    if st.text.startswith("RT @") or st.text.startswith("MT @"):
        return False

    # remove manual responses
    if st.text.startswith(".@"):
        return False

    # remove other spam tweets
    try:
        if spamFilter(st.text):
            return False
    except TypeError as e:
        # got this once, don't know why
        logger.warn(e)

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
        self._set_extra_entities()

        st = self._st

        self["sg_geolocalized"] = st.geo is not None
        self["sg_lang_%s" % st.lang] = 1
        self["sg_contributors"] = st.contributors is not None
        self["sg_emojis"] = contains_emoji(st.text)
        # some statuses don't have this attribute
        self["sg_nsfw"] = getattr(st, "possibly_sensitive", False)

        self["names"] = ",".join(extract_named_entities(st.text))

        self["retweet_count"] = getattr(st, "retweet_count", 0)
        self["favorite_count"] = getattr(st, "favorite_count", 0)

        for key in entity_keys:
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


    def _set_extra_entities(self):
        extra = {}

        media = getattr(self._st, "entities", {}).get("media", [])

        if media:
            photos = []

            for m in media:
                # TODO check the format for videos
                if m.get("type") != "photo":
                    continue
                photos.append({
                    # The image URL
                    "media_url": m["media_url_https"],
                    # The URL included in the status (expanded by us)
                    "url": m["expanded_url"],
                })

            extra["photos"] = photos

        self["extra_entities"] = dumps(extra)


def compute_features(status):
    expand_urls(status)
    f = FeaturesDict(status)
    f.compute_features()
    return f


def expand_urls(st):
    entities = getattr(st, "entities", {})
    for link in entities.get("urls", []) + entities.get("media", []):
        st.text = st.text.replace(link["url"], link["expanded_url"])
