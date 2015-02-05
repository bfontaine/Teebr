# -*- coding: UTF-8 -*-

from os import environ

from twitter import Api
from twitter.error import TwitterError

class TwitterAuthError(Exception):
    pass


class TwitterPipe(object):
    """
    A pipe between our app and Twitter, i.e. an object which fetchs tweets from
    Twitter and insert them in our database.
    """

    def __init__(self):
        self.init_from_env()


    def init_from_env(self, prefix="TWITTER_"):
        """
        Init the pipe from environment variables
        """
        keys = ("consumer_key", "consumer_secret", "access_token_key",
                "access_token_secret")

        kw = {k: environ["%s%s" % (prefix, k.upper())] for k in keys}
        self.api = Api(**kw)


    def check_credentials(self):
        """
        Check if the API credentials of this pipe are ok. It'll raise a
        ``TwitterAuthError`` if they aren't.
        """
        try:
            return self.api.VerifyCredentials()
        except TwitterError as t:
            if t.message[0].get("code") == 215:
                # Raise a proper exception
                raise TwitterAuthError(t.message)
            raise t
