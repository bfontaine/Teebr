# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from os import environ
from json import loads

from peewee import SqliteDatabase, Model
from peewee import FloatField, ForeignKeyField, BooleanField, CharField
from peewee import DateTimeField, IntegerField, PrimaryKeyField
import tweepy

db = SqliteDatabase(environ.get("TEEBR_SQLITE_DB_PATH", "db/teebr.db"))

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
    sg_media = IndicatorField(u"Media")

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


    # Hardcoded for the demo
    sg_mc_word_amazon       = IndicatorField("word:amazon")
    sg_mc_word_android      = IndicatorField("word:android")
    sg_mc_word_app          = IndicatorField("word:app")
    sg_mc_word_apple        = IndicatorField("word:apple")
    sg_mc_word_apps         = IndicatorField("word:apps")
    sg_mc_word_australia    = IndicatorField("word:australia")
    sg_mc_word_bbm          = IndicatorField("word:bbm")
    sg_mc_word_blog         = IndicatorField("word:blog")
    sg_mc_word_california   = IndicatorField("word:california")
    sg_mc_word_ceo          = IndicatorField("word:ceo")
    sg_mc_word_change       = IndicatorField("word:change")
    sg_mc_word_china        = IndicatorField("word:china")
    sg_mc_word_company      = IndicatorField("word:company")
    sg_mc_word_developer    = IndicatorField("word:developer")
    sg_mc_word_engadget     = IndicatorField("word:engadget")
    sg_mc_word_entrepreneur = IndicatorField("word:entrepreneur")
    sg_mc_word_everything   = IndicatorField("word:everything")
    sg_mc_word_facebook     = IndicatorField("word:facebook")
    sg_mc_word_food         = IndicatorField("word:food")
    sg_mc_word_fyi          = IndicatorField("word:fyi")
    sg_mc_word_galaxy       = IndicatorField("word:galaxy")
    sg_mc_word_google       = IndicatorField("word:google")
    sg_mc_word_green        = IndicatorField("word:green")
    sg_mc_word_happy        = IndicatorField("word:happy")
    sg_mc_word_interview    = IndicatorField("word:interview")
    sg_mc_word_ios          = IndicatorField("word:ios")
    sg_mc_word_ipad         = IndicatorField("word:ipad")
    sg_mc_word_iphone       = IndicatorField("word:iphone")
    sg_mc_word_ipod         = IndicatorField("word:ipod")
    sg_mc_word_itunes       = IndicatorField("word:itunes")
    sg_mc_word_java         = IndicatorField("word:java")
    sg_mc_word_life         = IndicatorField("word:life")
    sg_mc_word_linux        = IndicatorField("word:linux")
    sg_mc_word_love         = IndicatorField("word:love")
    sg_mc_word_macbook      = IndicatorField("word:macbook")
    sg_mc_word_microsoft    = IndicatorField("word:microsoft")
    sg_mc_word_mobile       = IndicatorField("word:mobile")
    sg_mc_word_music        = IndicatorField("word:music")
    sg_mc_word_netflix      = IndicatorField("word:netflix")
    sg_mc_word_nfl          = IndicatorField("word:nfl")
    sg_mc_word_night        = IndicatorField("word:night")
    sg_mc_word_nyt          = IndicatorField("word:nyt")
    sg_mc_word_office       = IndicatorField("word:office")
    sg_mc_word_people       = IndicatorField("word:people")
    sg_mc_word_phone        = IndicatorField("word:phone")
    sg_mc_word_product      = IndicatorField("word:product")
    sg_mc_word_programming  = IndicatorField("word:programming")
    sg_mc_word_python       = IndicatorField("word:python")
    sg_mc_word_reuters      = IndicatorField("word:reuters")
    sg_mc_word_review       = IndicatorField("word:review")
    sg_mc_word_school       = IndicatorField("word:school")
    sg_mc_word_seo          = IndicatorField("word:seo")
    sg_mc_word_social       = IndicatorField("word:social")
    sg_mc_word_software     = IndicatorField("word:software")
    sg_mc_word_someone      = IndicatorField("word:someone")
    sg_mc_word_startup      = IndicatorField("word:startup")
    sg_mc_word_startups     = IndicatorField("word:startups")
    sg_mc_word_store        = IndicatorField("word:store")
    sg_mc_word_sxsw         = IndicatorField("word:sxsw")
    sg_mc_word_tech         = IndicatorField("word:tech")
    sg_mc_word_technology   = IndicatorField("word:technology")
    sg_mc_word_tesla        = IndicatorField("word:tesla")
    sg_mc_word_thing        = IndicatorField("word:thing")
    sg_mc_word_touch        = IndicatorField("word:touch")
    sg_mc_word_tv           = IndicatorField("word:tv")
    sg_mc_word_twitter      = IndicatorField("word:twitter")
    sg_mc_word_uk           = IndicatorField("word:uk")
    sg_mc_word_video        = IndicatorField("word:video")
    sg_mc_word_watch        = IndicatorField("word:watch")
    sg_mc_word_web          = IndicatorField("word:web")
    sg_mc_word_windows      = IndicatorField("word:windows")
    sg_mc_word_women        = IndicatorField("word:women")
    sg_mc_word_work         = IndicatorField("word:work")
    sg_mc_word_world        = IndicatorField("word:world")
    sg_mc_word_youtube      = IndicatorField("word:youtube")


class User(ContentSignature):
    pass


class Producer(User):
    id_str = CharField(max_length=32, verbose_name=u"Twitter ID", unique=True)

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

    # These are used for tweets imports
    last_status_id = IntegerField(default=0)
    first_status_id = IntegerField(default=0)

    spam_reported_times = IntegerField(default=0)


class Consumer(User):
    screen_name = CharField(index=True, unique=True)

    language = CharField(default="en")

    # Cache
    rated_statuses = IntegerField(default=0)

    # Rights
    beta_features = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    def to_jsonable_dict(self):
        return {
            "rated_statuses": self.rated_statuses,
            "language": self.language,
            "beta_features": self.beta_features,
        }


class Status(ContentSignature):
    id_str = CharField(max_length=32, verbose_name=u"Twitter ID", unique=True)

    text = CharField()

    # Dates
    created_at = DateTimeField()

    # Location
    # FIXME not a text in Tweepy (use more fields?)
    #coordinates = CharField(null=True)
    lang = CharField(default="en", max_length=16)

    # FIXME not a text in Tweepy (use more fields?)
    #place = CharField(null=True)

    source = CharField()
    source_url = CharField()

    # Counts
    favorite_count = CountField()
    retweet_count = CountField()

    # Some more data we can use on the UI part. This is not used for the
    # classification.
    extra_entities = CharField(default="{}")

    author = ForeignKeyField(Producer, related_name='statuses')

    # experimental
    names = CharField()

    spam_reported_times = IntegerField(default=0)


class Rating(BaseModel):
    # -1: dislike, 1: like
    score = FloatField(default=0)

    status = ForeignKeyField(Status, related_name='ratings')
    consumer = ForeignKeyField(Consumer, related_name='ratings')


class TwitterCredentials(BaseModel):
    user = ForeignKeyField(Consumer, related_name='twitter_credentials')

    # for the app
    consumer_key = CharField()
    consumer_secret = CharField()
    # for the twitter user
    access_token_key = CharField()
    access_token_secret = CharField()

    def to_tweepy_oauth_handler(self):
        auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        return auth

    class Meta:
        indexes = (
            (('access_token_key', 'access_token_secret'), True),
        )


def create_tables():
    db.create_tables([
        Producer, Consumer, Status, Rating, TwitterCredentials], safe=True)


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


def status_to_dict(st):
    d = {
        "id": st.id,
        "text": st.text,
        # we want this to know if we need to hide extra entities that might be,
        # well, NSFW.
        "nsfw": st.sg_nsfw == 1,
        "extra_entities": loads(st.extra_entities),
        "expected": getattr(st, "expected_score", 0.0),
    }

    return d
