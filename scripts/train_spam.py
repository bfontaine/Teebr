# -*- coding: UTF-8 -*-

import datasets
import bayes

data = datasets.get("2015-03-11")
texts = [t.text for t in data]

storage = bayes.Storage("bayes.dat", 10)

try:
    storage.load()
except IOError:
    pass

bayes = bayes.Bayes(storage)

try:
    for text in texts:
        text = text.replace("\n", " ")
        print "==> %s" % text
        print ""
        resp = raw_input("Spam? [y/n] ")
        bayes.train(text, resp == "y")

finally:
    storage.finish()
