# -*- coding: UTF-8 -*-

import re
from string import punctuation as _punctuation

punctuation_re = re.compile("[%s]" % re.escape(
    re.sub(r"[-+_#$@']", "", _punctuation)))

# words/expressions that don't add info to a tweet
# Sources:
# - https://en.wikipedia.org/wiki/SMS_language#SMS_dictionaries
# - http://www.ranks.nl/stopwords
# - personal curation
stopwords_re = re.compile(r"\b(?:%s)\b" % "|".join([re.escape(word) for word in [
"'ll", "2day", "able", "about", "above", "abst", "accordance", "according",
"accordingly", "across", "act", "actually", "added", "adj", "afaik",
"affected", "affecting", "affects", "afk", "after", "afterwards", "again",
"against", "ah", "all", "almost", "alone", "along", "already", "also",
"although", "always", "am", "among", "amongst", "an", "and", "announce",
"another", "any", "anybody", "anyhow", "anymore", "anyone", "anything",
"anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren",
"aren't", "arent", "arise", "around", "as", "asap", "aside", "ask", "asking",
"at", "auth", "available", "away", "awfully", "b4", "back", "be", "became",
"because", "become", "becomes", "becoming", "been", "before", "beforehand",
"begin", "beginning", "beginnings", "begins", "behind", "being", "believe",
"below", "beside", "besides", "between", "beyond", "biol", "both", "brief",
"briefly", "but", "by", "ca", "came", "can", "can't", "cannot", "cant",
"cause", "causes", "certain", "certainly", "co", "com", "come", "comes",
"contain", "containing", "contains", "could", "couldn't", "couldnt", "date",
"december", "did", "didn't", "different", "do", "does", "doesn't", "doing",
"don't", "done", "down", "downwards", "due", "during", "each", "ed", "edu",
"effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end",
"ending", "enough", "especially", "et", "et-al", "etc", "even", "ever",
"every", "everybody", "everyone", "everything", "everywhere", "ex", "except",
"far", "february", "few", "ff", "fifth", "first", "five", "fix", "feb",
"thurs", "want", "'s", "wanted", "a lot", "or what", "wanna", "brb",
"followed", "following", "follows", "for", "former", "formerly", "forth",
"found", "four", "friday", "from", "further", "furthermore", "gave", "get",
"gets", "getting", "give", "given", "gives", "giving", "goes", "gone",
"good evening", "good morning", "got", "gotten", "had", "hadn't", "happens",
"hardly", "has", "hasn't", "have a nice day", "have", "haven't", "having",
"he", "he'd", "he'll", "he's", "hed", "hello", "hence", "her", "here",
"here's", "hereafter", "hereby", "herein", "heres", "hereupon", "hers",
"herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home",
"how", "how's", "howbeit", "however", "hundred", "i'd", "i'll", "i'm", "i've",
"ianal", "id", "ie", "if", "im", "imho", "immediate", "immediately", "imo",
"importance", "important", "in fact", "in", "inc", "indeed", "index",
"information", "instead", "into", "invention", "inward", "is", "isn't", "it",
"it'll", "it's", "itd", "its", "itself", "january", "july", "just", "keep",
"keeps", "kept", "kg", "km", "know", "known", "knows", "largely", "last",
"lately", "later", "latter", "latterly", "least", "less", "lest", "let",
"let's", "lets", "like", "liked", "likely", "line", "little", "lol", "lololol",
"look", "looking", "looks", "ltd", "made", "mainly", "make", "makes", "many",
"march", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile",
"merely", "mg", "might", "million", "miss", "ml", "monday", "more", "moreover",
"most", "mostly", "mr", "mrs", "much", "mug", "must", "mustn't", "my",
"myself", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily",
"necessary", "need", "needs", "neither", "never", "nevertheless", "new",
"next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless",
"noone", "nope", "nor", "normally", "nos", "not", "noted", "nothing",
"november", "now", "nowhere", "obtain", "obtained", "obviously", "of", "off",
"often", "oh", "ok", "okay", "old", "omg", "omitted", "on", "once", "one",
"ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought",
"our", "ours", "ourselves", "out", "outside", "over", "overall", "owing",
"own", "page", "pages", "part", "particular", "particularly", "past", "per",
"perhaps", "placed", "please", "plus", "plz", "poorly", "possible", "possibly",
"potentially", "pp", "predominantly", "present", "previously", "primarily",
"probably", "promptly", "pretty", "beautiful", "a year ago", "a yr ago",
"proud", "provides", "put", "que", "quickly", "quite", "qv", "ran", "rather",
"rd", "re", "readily", "really", "recent", "recently", "ref", "refs",
"regarding", "regardless", "regards", "related", "relatively", "research",
"respectively", "resulted", "resulting", "results", "right", "rofl", "rotfl",
"run", "said", "same", "saturday", "saw", "say", "saying", "says", "sec",
"section", "see ya", "see you", "see", "seeing", "seem", "seemed", "seeming",
"seems", "seen", "self", "selves", "sent", "seven", "several", "shall",
"shan't", "she", "she'd", "she'll", "she's", "shed", "shes", "should",
"shouldn't", "show", "showed", "shown", "showns", "shows", "significant",
"significantly", "similar", "similarly", "since", "six", "slightly", "so",
"some", "somebody", "somehow", "someone", "somethan", "something", "sometime",
"sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically",
"specified", "specify", "specifying", "still", "stop", "strongly", "sub",
"substantially", "successfully", "such", "sufficiently", "suggest", "sunday",
"sup", "sure", "than", "thank you", "thanks", "that", "that's", "the", "their",
"theirs", "them", "themselves", "then", "there", "there's", "these", "they",
"they'd", "they'll", "they're", "they've", "this", "thnx", "those", "through",
"thursday", "thx", "to", "today", "tomorrow", "too", "ttyl", "tuesday",
"under", "until", "up", "very", "w/", "w/out", "was", "wasn't", "wdymbt", "we",
"we'd", "we'll", "we're", "we've", "wednesday", "were", "weren't", "what",
"what's", "when", "when's", "where", "where's", "which", "while", "who",
"who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "ya",
"yeah", "yes", "yesterday", "you", "you'd", "you'll", "you're", "you've",
"your", "yours", "yourself", "yourselves", "wtf", "wth", "pls", "via", "a",
"u", "gf", "stfu", "shut up", "asshole",
]]), re.IGNORECASE)

sounds_re = re.compile(r"\b(?:%s)\b" % "|".join([word for word in [
    "(?:ha){2,}"
]]), re.IGNORECASE)
