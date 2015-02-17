# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from .models import Status, create_tables
from .features import compute_features


def init():
    create_tables()


# dead simple for now
# TODO extract the status' author
def import_status(st):
    """
    Import a status in the DB
    """
    feat = compute_features(st)
    s = Status(**feat)
    s.save()
    return s


def rate_status(consumer, status, score):
    # TODO
    pass
