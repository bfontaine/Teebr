# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from os import environ

import tweepy

from .features import filter_status
from .log import mkLogger
from .pipeline import import_status, init

logger = mkLogger("pipe")

class TwitterPipeListener(tweepy.StreamListener):

    def __init__(self, *args, **kw):
        super(TwitterPipeListener, self).__init__(*args, **kw)
        init()

    def on_status(self, status):
        if not filter_status(status):
            return
        logger.debug("Importing status id '%s'" % status.id)
        import_status(status)


class TwitterPipe(object):

    def __init__(self):
        self.init_from_env()


    def init_from_env(self, prefix="TWITTER_"):
        """
        Init the pipe from environment variables
        """
        keys = ("consumer_key", "consumer_secret", "access_token_key",
                "access_token_secret")

        kw = {k: environ["%s%s" % (prefix, k.upper())] for k in keys}

        # see https://github.com/tweepy/examples/blob/master/streamwatcher.py
        # for an example on how to create a stream handler
        auth = tweepy.auth.OAuthHandler(kw["consumer_key"],
                kw["consumer_secret"])
        auth.set_access_token(kw["access_token_key"], kw["access_token_secret"])
        self.stream = tweepy.Stream(auth, TwitterPipeListener(), timeout=None)


    def run(self):
        try:
            # we'll filter users/keywords later
            self.stream.sample()
        except KeyboardInterrupt:
            logger.debug("Stopping the API pipe due to keyboard interrupt")


def collect():
    t = TwitterPipe()
    t.run()
