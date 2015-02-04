# -*- coding: UTF-8 -*-

from os import environ
from pyelasticsearch import ElasticSearch

# base module

class Store(object):

    def __init__(self):
        self._es = None

    def es(self):
        if not self._es:
            self._es = ElasticSearch(self.get_url())
        return self._es

    def get_url(self):
        return environ.get("ELASTICSEARCH_URL", "http://localhost:9200")

    def get_user(self, *args, **kwargs):
        return None  # TODO

    # ES Methods
    # -------------------------------------------------------------------------

    def health(self):
        return self.es().health()


store = Store()
