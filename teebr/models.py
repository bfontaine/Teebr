# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from os import environ
from peewee import SqliteDatabase, Model
from peewee import FloatField, ForeignKeyField, BooleanField, CharField
from peewee import DateTimeField, IntegerField, PrimaryKeyField

db = SqliteDatabase(environ.get("TEEBR_SQLITE_DB_PATH", "/tmp/teebr.db"))

class IndicatorField(FloatField):
    def __init__(self, name, **kwargs):
        kwargs.setdefault("default", 0)
        kwargs.setdefault("verbose_name", name)
        super(IndicatorField, self).__init__(**kwargs)


class HexColorField(CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 6)
        super(HexColorField, self).__init__(**kwargs)


class CountField(IntegerField):
    def __init__(self, **kwargs):
        kwargs.setdefault("default", 0)
        super(CountField, self).__init__(**kwargs)


class BaseModel(Model):
    class Meta:
        database = db


class ContentSignature(BaseModel):

    # Sources
    sg_source_mobile = IndicatorField(u"Mobile source")
    sg_source_tablet = IndicatorField(u"Tablet source")
    sg_source_desktop = IndicatorField(u"Desktop source")
    sg_source_autopub = IndicatorField(u"Autopub source")
    sg_source_social = IndicatorField(u"Social source")
    sg_source_news = IndicatorField(u"News source")
    sg_source_others = IndicatorField(u"Other source")

    # URLs
    sg_url_social = IndicatorField(u"Social URL")
    sg_url_social_media = IndicatorField(u"Social Media URL")
    sg_url_product = IndicatorField(u"Product URL")
    sg_url_video = IndicatorField(u"Video URL")

    # Entities
    sg_urls = IndicatorField(u"URLs")
    sg_hashtags = IndicatorField(u"Hashtags")
    sg_user_mentions = IndicatorField(u"Mentions")
    sg_trends = IndicatorField(u"Trends")
    sg_symbols = IndicatorField(u"Symbols")

    # L10N
    sg_geolocalized = IndicatorField(u"Geolocalized")

    # Languages
    sg_lang_en = IndicatorField(u"English")
    sg_lang_fr = IndicatorField(u"French")

    # Content
    sg_emojis = IndicatorField(u"Emojis")
    sg_nsfw = IndicatorField(u"NSFW")

    # Other Twitter features
    sg_contributors = IndicatorField(u"Contributors")


class User(ContentSignature):
    pass


class Producer(User):
    id_str = CharField(max_length=32, verbose_name=u"Twitter ID")

    protected = BooleanField(default=False)
    verified = BooleanField(default=False)
    is_translator = BooleanField(default=False)

    # Text
    name = CharField()
    screen_name = CharField(index=True, unique=True)
    description = CharField(null=True)

    # Location
    geo_enabled = BooleanField(default=False)
    lang = CharField(default="en", max_length=16)
    location = CharField(null=True)
    time_zone = CharField(null=True)
    utc_offset = IntegerField(null=True)

    url = CharField(null=True)

    # Dates
    created_at = DateTimeField()

    # Counts
    favourites_count = CountField()
    followers_count = CountField()
    friends_count = CountField()
    listed_count = CountField()
    statuses_count = CountField()

    # Profil colors
    profile_background_color = HexColorField()
    profile_link_color = HexColorField()
    profile_sidebar_border_color = HexColorField()
    profile_sidebar_fill_color = HexColorField()
    profile_text_color = HexColorField()

    # Profil images
    profile_background_image_url_https = CharField(null=True, verbose_name=u"Background image URL")
    profile_image_url_https = CharField(null=True, verbose_name=u"Avatar URL")

    default_profile = BooleanField(default=True)
    default_profile_image = BooleanField(default=True)
    profile_use_background_image = BooleanField(default=False)

    # Misc Twitter features
    contributors_enabled = BooleanField(default=False)

    # Cache
    imported_statuses = IntegerField(default=0)


class Consumer(User):

    # Cache
    rated_statuses = IntegerField(default=0)


class Status(ContentSignature):
    id_str = CharField(max_length=32, verbose_name=u"Twitter ID")

    text = CharField()

    # Dates
    created_at = DateTimeField()

    # Location
    coordinates = CharField(null=True)
    lang = CharField(default="en", max_length=16)

    # FIXME not a text in Tweepy (use more fields?)
    place = CharField(null=True)

    source = CharField()
    source_url = CharField()

    # Counts
    favorite_count = CountField()
    retweet_count = CountField()

    entities_json = CharField(default="{}")

    author = ForeignKeyField(Producer, related_name='statuses')


class Rating(BaseModel):
    # -1: dislike, 1: like
    score = FloatField(default=0)

    status = ForeignKeyField(Status, related_name='ratings')
    consumer = ForeignKeyField(Consumer, related_name='ratings')


def create_tables():
    db.create_tables([ Producer, Consumer, Status, Rating ], safe=True)


def dict2model(kv, model, create=False):
    """
    Take a dictionnary and a model class and return a new model instance
    """
    params = {}
    for k,v in model._meta.fields.items():
        # don't override 'id' nor any foreign key
        if not isinstance(v, ForeignKeyField) \
                and not isinstance(v, PrimaryKeyField) \
                and k in kv:
            params[k] = kv[k]
    if create:
        return model.create(**params)
    return model(**params)
