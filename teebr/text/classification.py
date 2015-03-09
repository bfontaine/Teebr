# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

import re
import yaml
from collections import defaultdict

from ..log import mkLogger

__all__ = ["TextClassifier"]

logger = mkLogger("classifier")

class Rule(object):
    __slots__ = ["name", "meta", "patterns", "compiled", "reject"]

    # patterns: score => patterns
    def __init__(self, name, meta, patterns, reject=[]):
        self.name = name
        self.meta = meta
        self.patterns = []
        self.compiled = False
        self.compile_patterns(patterns, reject)

    def compile_patterns(self, patterns, reject=[]):
        if self.compiled:
            return
        for score, regs in patterns.items():
            if not regs:
                continue
            reg = "|".join([re.escape(r) for r in regs])
            self.patterns.append((score,  re.compile(r"\b(?:%s)\b" % reg)))

        rej = "|".join([re.escape(r) for r in reject])
        rej = re.compile(r"(?:%s)" % rej)

        self.patterns = tuple(self.patterns)
        self.reject = rej
        self.compiled = True

    def match(self, text):
        """
        Return a matching score
        """
        if self.reject.search(text):
            return 0

        s = 0
        for score, patt in self.patterns:
            for _ in patt.finditer(text):
                s += score
        return s


class TextClassifier(object):
    __slots__ = ["categories", "rules"]

    def __init__(self, rules_file):
        self.rules = set()

        self.import_rules(rules_file)

    def import_rules(self, rules_file):
        with open(rules_file) as f:
            for name, spec in yaml.load(f.read()).items():
                meta = spec.get("meta", [])
                exprs = spec.get("expressions", [])
                words = spec.get("words", [])
                reject = spec.get("reject", [])
                self.rules.add(Rule(name, meta, {
                    100: exprs,
                    20: words,
                }, reject))

    def classify(self, text):
        matches = defaultdict(int)
        for r in self.rules:
            score = r.match(text)

            matches[r.name] += score
            for cat in r.meta:
                matches[cat] += score

        return matches
