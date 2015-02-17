# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from os import environ
from peewee import SqliteDatabase, Model
from peewee import FloatField, ForeignKeyField, BooleanField

db = SqliteDatabase(environ.get("TEEBR_SQLITE_DB_PATH", "/tmp/wsw.db"))

class IndicatorField(FloatField):
    def __init__(self, **kwargs):
        kwargs.setdefault("default", 0)
        super(IndicatorField, self).__init__(**kwargs)


class BaseModel(Model):
    class Meta:
        database = db


class ContentSignatureMixin(BaseModel):

    # Sources
    source_mobile = IndicatorField()
    source_tablet = IndicatorField()
    source_desktop = IndicatorField()
    source_autopub = IndicatorField()
    source_social = IndicatorField()
    source_news = IndicatorField()
    source_others = IndicatorField()

    # URLs
    url_social = IndicatorField()
    url_social_media = IndicatorField()
    url_product = IndicatorField()
    url_video = IndicatorField()

    # Entities
    urls = IndicatorField()
    hashtags = IndicatorField()
    mentions = IndicatorField()

    # L10N
    geolocalized = IndicatorField()

    # Languages
    lang_en = IndicatorField()
    lang_fr = IndicatorField()

    emojis = IndicatorField()

    # Other Twitter features
    contributors = IndicatorField()


class User(BaseModel):
    pass


class Producer(User, ContentSignatureMixin):
    pass


class Consumer(User, ContentSignatureMixin):
    pass


class Status(BaseModel, ContentSignatureMixin):
    pass


class Rating(BaseModel):
    score = BooleanField()

    tweet = ForeignKeyField(Status, related_name='ratings')
    user = ForeignKeyField(Consumer, related_name='ratings')


def create_tables():
    db.create_tables([ Producer, Consumer, Status ], safe=True)
