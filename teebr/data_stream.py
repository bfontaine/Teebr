# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from json import dumps

import tweepy

from .config import config
from .features import filter_status, LANGUAGES
from .log import mkLogger
from .models import TwitterCredentials
from .pipeline import import_status, init_pipeline

logger = mkLogger("data")

class TwitterRawPipeListener(tweepy.StreamListener):
    """
    A pipe listener which dumps all tweets in a file
    """

    def __init__(self, *args, **kw):
        super(TwitterRawPipeListener, self).__init__(*args, **kw)
        self.output = open("raw_tweets.jsons", "a")

    def on_status(self, status):
        self.output.write(u"%s\n" % unicode(dumps(status._json)))


class TwitterPipeListener(tweepy.StreamListener):

    def __init__(self, *args, **kw):
        super(TwitterPipeListener, self).__init__(*args, **kw)
        init_pipeline()

    def on_status(self, status):
        if not filter_status(status):
            return
        import_status(status)

    def on_error(self, status_code):
        print "Error %s" % status_code
        logger.warn("Error: got a status code %s, stopping" % status_code)
        return False


class TwitterPipe(object):

    def __init__(self, raw=False):
        self.raw = raw
        self.init_from_db()

    def init_from_env(self, prefix="TWITTER_"):
        """
        Init the pipe from environment variables
        """
        keys = ("consumer_key", "consumer_secret", "access_token_key",
                "access_token_secret")

        kw = {k: config["%s%s" % (prefix, k.upper())] for k in keys}

        # see https://github.com/tweepy/examples/blob/master/streamwatcher.py
        # for an example on how to create a stream handler
        auth = tweepy.auth.OAuthHandler(kw["consumer_key"],
                kw["consumer_secret"])
        auth.set_access_token(kw["access_token_key"], kw["access_token_secret"])
        self.init_stream(auth)

    def init_from_db(self):
        """
        Init the pipe from credentials found in the DB
        """
        auth = TwitterCredentials.get().to_tweepy_oauth_handler()
        self.init_stream(auth)

    def init_stream(self, auth):
        klass = TwitterPipeListener if not self.raw else TwitterRawPipeListener

        self.stream = tweepy.Stream(auth, klass(), timeout=None)


    def run(self, follow_ids=None, keywords=None):
        params = {"languages": LANGUAGES}
        filters = False

        if follow_ids is not None:
            logger.debug("Following %d ids" % len(follow_ids))
            filters = True
            params["follow"] = follow_ids

        if keywords is not None:
            logger.debug("Tracking %d keywords" % len(keywords))
            filters = True
            params["track"] = keywords

        logger.debug("Starting the pipeline...")
        try:
            if filters:
                self.stream.filter(**params)
            else:
                self.stream.sample(**params)
            logger.debug("End of the pipeline")
        except KeyboardInterrupt:
            logger.debug("Stopping the API pipe due to keyboard interrupt")


def collect(raw=False, **kw):
    t = TwitterPipe(raw=raw)
    t.run(**kw)
