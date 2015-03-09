# -*- coding: UTF-8 -*-

from json import loads
from tweepy.models import Status
from glob import glob

_prefix = "datasets/statuses-"
_suffix = ".jsons"

_prefix_len = len(_prefix)
_suffix_len = len(_suffix)

def list():
    return [s[_prefix_len:-_suffix_len] \
            for s in glob("%s*%s" % (_prefix, _suffix))]

def get(name, mx=10000):
    ss = []
    with open("datasets/statuses-%s.jsons" % name) as f:
        for i, l in enumerate(f):
            if i > mx:
                break
            ss.append(Status.parse(None, loads(l)))
    return ss
