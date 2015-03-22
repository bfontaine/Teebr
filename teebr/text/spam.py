# -*- coding: UTF-8 -*-

import bayes

storage = bayes.Storage("bayes.dat", 10)
storage.load()

def is_spam(text):
    try:
        return bayes.Bayes(storage).is_spam(text)
    except TypeError:
        # This sometimes happen on small texts, don't know how to fix that:
        #     File ".../bayes.py", line 155, in spam_rating
        #         p = reduce(operator.mul, ratings)
        #     TypeError: reduce() of empty sequence with no initial value
        return False
