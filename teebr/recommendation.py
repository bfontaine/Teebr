# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from .text.utils import most_common_words

# Note: we could also adjust these depending on the rarity of each feature. For
# example, a very rare feature could have a high factor while a more common one
# would have a lower factor.
# The default factor is 1.0. Most of the values below are arbitrary.
feat_factors = {
    'sg_source_social': 2.0,
    'sg_source_news': 2.0,

    'sg_url_social': 2.0,
    'sg_url_social_media': 2.0,

    'sg_urls': 3.0,
    'sg_hashtags': 1.5,
    'sg_user_mentions': 2.0,
    'sg_trends': 2.0,
    'sg_symbols': 3.0,
    'sg_media': 3.0,

    'sg_geolocalized': 1.2,

    'sg_lang_en': 3.0,
    'sg_lang_fr': 3.0,

    'sg_emoji': 2.0,
    'sg_nsfw': 2.0,
}

for mcw in most_common_words:
    feat_factors["sg_mc_word_%s" % mcw] = 3.0


def similarity_score(keys, sig1, sig1_count, sig2, sig2_count):
    """
    Compute a similarity score between two signatures.
    """
    score = 0.0
    factors = 0.0

    if keys is None:
        keys = sig1._meta.fields.keys()

    sig1 = sig1.__dict__["_data"]
    sig2 = sig2.__dict__["_data"]

    sig1_count = float(sig1_count)
    sig2_count = float(sig2_count)

    for k in keys:
        if not k.startswith("sg_"):
            continue

        v1 = sig1[k]
        v2 = sig2[k]

        # we don't compare on a feature if one signature has a null value
        if v1 == 0 or v2 == 0:
            continue

        if v1 < -1.0:
            v1 = -1.0

        if v2 < -1.0:
            v2 = -1.0

        # normalize both features
        v1 /= sig1_count
        v2 /= sig2_count

        factor = feat_factors.get(k, 1.0)

        score += (abs(v2 - v1) * factor)
        factors += factor

    if factors == 0:
        return 1.0

    # we'd have to divide by 2 because ratings can be negative: [-1, +1] but we
    # now use non-negative ratings (see in teebr.pipeline.rate_status)
    return score / factors

def users_similarity_score(consumer, producer):
    """
    Compute a similarity score between a consumer's and a producer's
    signatures. The score is a float between 0 (complete similarity) and 1
    (nothing in common).
    """
    count_consumer = float(consumer.rated_statuses)
    count_producer = float(producer.imported_statuses)

    return similarity_score(
            None, consumer, count_consumer, producer, count_producer)
