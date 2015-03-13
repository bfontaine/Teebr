# -*- coding: UTF-8 -*-
from sys import argv
from teebr.data import collect

def read_words(path):
    with open(path) as f:
        words = []
        for k in f:
            k = k.strip().split(" ", 2)[0]
            if k:
                words.append(k)
    return words


kw = read_words("keywords.txt")
accounts = read_words("accounts.txt")

raw = False

if len(argv) > 1 and argv[1] == "raw=true":
    print "Collecting raw tweets..."
    raw = True

collect(raw=raw, keywords=kw, follow_ids=accounts)
