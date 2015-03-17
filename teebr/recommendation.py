# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

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

def similarity_score(consumer, producer):
    """
    Compute a similary score between two signatures. The score is a float
    between 0 (complete similarity) and 1 (nothing in common).
    """
    score = 0.0
    factors = 0.0

    feats_consumer = consumer._meta.fields.items()
    feats_producer = producer._meta.fields.items()

    count_consumer = float(consumer.rated_statuses)
    count_producer = float(producer.imported_statuses)

    for k, vc in feats_consumer:
        if not k.startswith("sg_"):
            continue

        vp = feats_producer[k]

        # we don't compare on a feature if one signature has a null value
        if vc == 0 or vp == 0:
            continue

        factor = feat_factors.get(k, 1.0)

        # normalize both features
        vc /= count_consumer
        vp /= count_producer

        score += abs(vp - vc) * factor
        factors += factor

    if factors == 0:
        return 1.0

    return score / factors
