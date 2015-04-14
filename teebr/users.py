# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import fn

from .log import mkLogger
from .models import Status, Consumer, Producer, db
from .recommendation import similarity_score, users_similarity_score
from .web import get_languages

logger = mkLogger("users")

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

    # PERF This could be optimized, we're using quick & dirty code for now

    ratings = list(user.ratings)
    raw_statuses = Status.select().order_by(fn.Random()).limit(count*2)

    add_expected_score = user.beta_features

    feat_keys = user._meta.fields.keys()
    feats_user_count = float(user.rated_statuses)

    statuses = []
    for st in raw_statuses:
        for rt in ratings:
            if rt.status == st:
                ratings.remove(rt)
                continue

        if add_expected_score:
            score = users_similarity_score(user, st.author)
            #score = similarity_score(feat_keys, user, feats_user_count, st, 1)
            setattr(st, "expected_score", score)

        statuses.append(st)
        count -= 1
        if count <= 0:
            break

    return statuses


def mark_status_as_spam(status_id):
    st = Status.get(Status.id == status_id)

    st.spam_reported_times += 1

    # PERF N+1 query here
    st.author.spam_reported_times += 1

    if st.author.spam_reported_times >= 5:
        st.author.delete_instance(recursive=True)
        return

    st.author.save()

    if st.spam_reported_times >= 3:
        st.delete_instance(recursive=True)
        return

    st.save()


def set_user_settings(consumer, settings):
    language = settings["language"]
    beta = settings["beta_features"]
    consumer.beta_features = bool(beta)

    if consumer.language == language or language not in get_languages(True):
        consumer.save()
        return False

    # we reload only if the language changed
    consumer.language = language
    consumer.save()
    return True


def reset_user_ratings(consumer):
    screen_name = consumer.screen_name

    # delete
    consumer.delete_instance(recursive=True)

    # re-create
    get_consumer_profile(screen_name)


def get_similar_producers(consumer, limit=5, min_statuses=10, max_threshold=0.5):
    """
    Retrieve the top producers by their similarity with the given consumer.
    This is an expensive computation and could be optimized in the future.
    """
    producers = Producer.select().where(Producer.imported_statuses > min_statuses)
    producers = producers.order_by(fn.Random()).limit(max(2000, limit*2))

    raw_producers = []

    for producer in producers:
        score = users_similarity_score(consumer, producer)
        if score <= max_threshold:
            raw_producers.append((score, producer))

    raw_producers.sort(key=lambda p: p[0])

    if limit <= 0:
        # sane default
        limit = 5

    return raw_producers[:limit]
