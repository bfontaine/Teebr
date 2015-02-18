# -*- coding: UTF-8 -*-
from teebr.data import collect

with open("keywords.txt") as f:
    kw = [k.strip() for k in f if k.strip()]

collect(keywords=kw)
