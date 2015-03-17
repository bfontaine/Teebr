# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from .models import TwitterCredentials

def get_tweepy_oauth_handler():
    return TwitterCredentials.get().to_tweepy_oauth_handler()
