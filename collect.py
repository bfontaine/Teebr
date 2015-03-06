# -*- coding: UTF-8 -*-
from sys import argv
from teebr.data import collect

with open("keywords.txt") as f:
    kw = [k.strip() for k in f if k.strip()]

raw = False

if len(argv) > 1 and argv[1] == "raw=true":
    print "Collecting raw tweets..."
    raw = True

collect(raw=raw, keywords=kw)
