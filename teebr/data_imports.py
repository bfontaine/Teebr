# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from peewee import IntegrityError

from .web.oauth import twitter
from .models import TwitterCredentials
from .log import mkLogger
from .pipeline import init_pipeline

logger = mkLogger("data_imports")

init_pipeline()

def import_credentials(consumer, creds):
    if consumer is None or creds is None:
        return

    token, secret = creds

    tc = TwitterCredentials.create(
        user=consumer,
        consumer_key=twitter.consumer_key,
        consumer_secret=twitter.consumer_secret,
        access_token_key=token,
        access_token_secret=secret)

    try:
        tc.save()
    except IntegrityError as e:
        logger.warn(e)
