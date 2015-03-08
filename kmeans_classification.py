# -*- coding: UTF-8 -*-

# Just a test based on
# http://scikit-learn.org/stable/auto_examples/document_clustering.html

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

from sklearn.cluster import MiniBatchKMeans

from json import loads
from tweepy.models import Status

from teebr.text.utils import normalize_text
from teebr.features import filter_status

CLUSTERS = 40
DIMS = 100

tweets = []

tw_count = 0

with open("raw_tweets.jsons") as f:
    for line in f:
        j = loads(line)
        t = Status.parse(None, j)
        if filter_status(t):
            tweet = normalize_text(t.text)
            tweets.append(tweet)
            tw_count += 1
            if tw_count >= 12000:
                break

# less tweets for the tests
#tweets = tweets[:10000]

print "tweets: %d" % len(tweets)

#hasher = HashingVectorizer(stop_words='english', non_negative=True, norm=None)
#vectorizer = make_pipeline(hasher, TfidfTransformer())

vectorizer = TfidfVectorizer(max_df=0.8, max_features=2**32,
                             min_df=0.001, stop_words='english',
                                 use_idf=True)

X = vectorizer.fit_transform(tweets)

print "shape: %d %d" % X.shape

# arbitrary
svd = TruncatedSVD(X.shape[1]/2) #TruncatedSVD(DIMS)
lsa = make_pipeline(svd, Normalizer(copy=False))
X = lsa.fit_transform(X)

print "starting the kmeans"

# km = KMeans(max_iter=2, n_init=1, verbose=True, precompute_distances=True,
#         n_jobs=-3)

km = MiniBatchKMeans(verbose=False, n_clusters=CLUSTERS)

km.fit(X)

print "done"

print "Top terms per cluster:"
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(CLUSTERS):
    print "  Cluster %d:" % i
    for ind in order_centroids[i, :40]:
        print "   - %s" % terms[ind]
