# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import IntegrityError, fn

from .features import compute_features
from .log import mkLogger
from .models import create_tables, dict2model
from .models import Status, Consumer, Producer, Rating, db

logger = mkLogger("pipeline")

def init_pipeline():
    logger.debug("Creating tables")
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


def get_consumer_profile(screen_name):
    if screen_name is None:
        return None

    with db.transaction():
        try:
            consumer = Consumer.get(Consumer.screen_name == screen_name)
        except Consumer.DoesNotExist:
            logger.debug("Creating user '%s'" % screen_name)
            consumer = Consumer.create(screen_name=screen_name)
            consumer.save()
        return consumer


def get_unrated_statuses(user, count=20):
    """
    Return a random sample of statuses unrated by ``user`` of max ``count``.
    """

    # This could be optimized, we're using quick & dirty code for now

    ratings = user.ratings
    raw_statuses = Status.select().order_by(fn.Random()).limit(count*2)

    statuses = []
    for st in raw_statuses:
        for rt in ratings:
            if rt.status == st:
                ratings.remove(rt)
                continue
        statuses.append(st)
        count -= 1
        if count <= 0:
            break

    return statuses


def rate_status(consumer, status_id, score):
    status = Status.get(Status.id == Status.id)

    with db.transaction():
        r = Rating.create(consumer=consumer, status=status, score=score)
        consumer.rated_statuses += 1
        r.save()

        update_user_sg_from_status(consumer, status, score)
        consumer.save()


def mark_status_as_spam(status_id):
    # TODO
    pass


def reset_user_ratings(consumer):
    screen_name = consumer.screen_name

    # delete
    consumer.delete_instance(recursive=True)

    # re-create
    get_consumer_profile(screen_name)
