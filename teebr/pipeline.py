# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import IntegrityError

from .features import compute_features
from .log import mkLogger
from .models import create_tables, dict2model, Rating, Status, Producer, db

logger = mkLogger("pipeline")

def init_pipeline():
    logger.debug("Creating tables")
    create_tables()


def import_status(st, author=None):
    """
    Import a status in the DB
    """
    st_dict = st.__dict__
    author_dict = st.author.__dict__

    st_dict.update(compute_features(st))

    with db.transaction():
        if not author:
            # get or create on the author
            save_author = False
            try:
                author = dict2model(author_dict, Producer, True)
                save_author = True
            except IntegrityError as e:
                logger.debug(e)
                author = Producer.get(Producer.screen_name == author_dict["screen_name"])

            if save_author:
                author.save()

        # get or create on the status
        try:
            status = Status.get(Status.id_str == st_dict["id_str"])
        except Status.DoesNotExist:
            status = dict2model(st_dict, Status)

        set_producer(author, status, st_dict)
        status.save()

    #logger.debug("Imported status '%s' as '%s'" % (status.id_str, status.id))

    return status


def update_user_sg_from_dict(user, st_dict, factor=1):
    factor = float(factor)
    d_u = user.__dict__["_data"]
    for k,v in st_dict.items():
        if k.startswith("sg_"):
            d_u[k] += v * factor


def update_user_sg_from_status(user, st, factor=1):
    factor = float(factor)
    d_u = user.__dict__["_data"]
    st_dict = st.__dict__["_data"]
    for k,v in st_dict.items():
        if k.startswith("sg_"):
            d_u[k] += v * factor


def set_producer(producer, status, st_dict):
    status.author = producer
    update_user_sg_from_dict(producer, st_dict, 1)

    producer.imported_statuses += 1
    producer.save()


def rate_status(consumer, status_id, score):
    status = Status.get(Status.id == Status.id)

    with db.transaction():
        r = Rating.create(consumer=consumer, status=status, score=score)
        consumer.rated_statuses += 1
        r.save()

        update_user_sg_from_status(consumer, status, score)
        consumer.save()

    # TODO validate our model: check similarity_score between the consumer and
    # the status and see if the score was expected or not (e.g. positive score
    # and good score = good, everything else is bad)
