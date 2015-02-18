# -*- coding: UTF-8 -*-

from json import loads
from tweepy.models import Status

def get(name, mx=10000):
    ss = []
    with open("datasets/statuses-%s.jsons" % name) as f:
        for i, l in enumerate(f):
            if i > mx:
                break
            ss.append(Status.parse(None, loads(l)))
    return ss
