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
    save_author = False
    with db.transaction():
        try:
            author = dict2model(author_dict, Producer, True)
            save_author = True
        except IntegrityError as e:
            logger.debug(e)
            author = Producer.get(Producer.screen_name == author_dict["screen_name"])

        if save_author:
            author.save()

        status = dict2model(st_dict, Status)
        set_producer(author, status, st_dict)

        status.save()

    logger.debug("Imported status '%s' as '%s'" % (status.id_str, status.id))

    return status


def update_user_sg(user, st_dict, factor=1):
    factor = float(factor)
    d_u = user.__dict__["_data"]
    for k,v in st_dict.items():
        if k.startswith("sg_"):
            d_u[k] += v * factor


def set_producer(producer, status, st_dict):
    status.author = producer
    update_user_sg(producer, st_dict, 1)

    producer.imported_statuses += 1
    producer.save()


def rate_status(consumer, status, st_dict, score):
    with db.transaction():
        r = Rating.create(consumer=consumer, status=status, score=score)
        consumer.rated_statuses += 1
        r.save()

        update_user_sg(consumer, st_dict, score)
        consumer.save()
