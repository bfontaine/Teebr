# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from peewee import IntegrityError
from tweepy.api import API as TwitterAPI
#from tweepy.error import TweepError

from .auth import get_tweepy_oauth_handler
from .web.oauth import twitter
from .models import TwitterCredentials, Producer
from .log import mkLogger
from .features import filter_status
from .pipeline import import_status, init_pipeline

logger = mkLogger("data_imports")

# This has to be <=200
STATUSES_PER_PRODUCER = 50

init_pipeline()

def import_credentials(consumer, creds):
    if consumer is None or creds is None:
        return

    token, secret = creds

    try:
        TwitterCredentials.create(
            user=consumer,
            consumer_key=twitter.consumer_key,
            consumer_secret=twitter.consumer_secret,
            access_token_key=token,
            access_token_secret=secret)
    except IntegrityError as e:
        logger.warn(e)


class TimelinesFetcher(object):
    def __init__(self):
        auth = get_tweepy_oauth_handler()
        # This could be optimized once we have more than one credentials set in
        # the DB (we could loop over them).
        self.api = TwitterAPI(auth_handler=auth,
                wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def start(self):
        while True:
            for producer in Producer.select():
                self.fetch_producer(producer)

    def fetch_producer(self, producer):
        # 200 is the page limit
        kwargs = {"count": STATUSES_PER_PRODUCER, "user_id": producer.id_str}

        if producer.last_status_id != 0:
            kwargs["since_id"] = producer.last_status_id

        #try:
        timeline = list(self.api.user_timeline(**kwargs))
        #except TweepError as e:
        #    logger.warn(e)
        #    return

        logger.debug("Importing %d statuses from @%s" % (
            len(timeline), producer.screen_name))

        if timeline:
            for st in timeline:
                self.on_status(producer, st)

            producer.last_status_id = timeline[-1].id
            producer.save()

    def on_status(self, producer, status):
        if filter_status(status):
            import_status(status, author=producer)
            return True

def fetch_user_timelines():
    tf = TimelinesFetcher()

    try:
        tf.start()
    except KeyboardInterrupt:
        logger.debug("Stoping user timelines fetching due to ^C")
