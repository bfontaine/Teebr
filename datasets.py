# -*- coding: UTF-8 -*-

from json import loads
from tweepy.models import Status

def get(name):
    with open("datasets/statuses-%s.jsons" % name) as f:
        return [Status.parse(None, loads(l)) for l in f]
