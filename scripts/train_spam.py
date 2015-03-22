# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import datasets
import bayes
from sys import argv

if len(argv) == 2:
    with open(argv[1]) as f:
        texts = [l.strip() for l in f]
else:
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
