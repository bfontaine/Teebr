# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import IntegrityError

from .features import compute_features
from .log import mkLogger
from .models import create_tables, dict2model
from .models import Status, Producer, Rating, db

logger = mkLogger("pipeline")

def init_pipeline():
    create_tables()


def import_status(st):
    """
    Import a status in the DB
    """
    st_dict = st.__dict__
    author_dict = st.author.__dict__

    st_dict.update(compute_features(st))

    # get or create
    with db.transaction():
        try:
            author = dict2model(author_dict, Producer, True)
        except IntegrityError as e:
            logger.debug(e)
            author = Producer.get(Producer.screen_name == author_dict["screen_name"])

        author.save()

    status = dict2model(st_dict, Status)
    status.author = author

    status.save()

    logger.debug("Imported status '%s' as '%s'" % (status.id_str, status.id))

    return status


def rate_status(consumer, status, score):
    # TODO update the consumer's signature
    with db.transaction():
        r = Rating.create(consumer=consumer, status=status, score=score)
        consumer.rated_statuses += 1
        r.save()
        consumer.save()
