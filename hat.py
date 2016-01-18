#/usr/bin/python3
import collections
import json
import string
import os

from .hlpConstants import HLPDIR, DICT_FNAMES, NUMERICALS_FNAME

class Hat(object):
    ALPHABET = string.ascii_uppercase
    def __init__(self, numericals_fname=None, dict_fnames=None):
        self.numericals = collections.defaultdict(set)
        self.readin_numerical(numericals_fname) or self.readin_dict(dict_fnames)

    def numerizeWord(self, word):
        numeric = [None] * len(word) ## tuple-ize after assignments
        offset = 1
        for letter, counts in sorted(collections.Counter(word).items()):
            occurrence = -1
            for count in range(counts):
                occurrence = word.find(letter, occurrence + 1)
                numeric[occurrence] = offset
                offset += 1
        return tuple(numeric)
    
    def findWords(self, indices, two_words=True):
        answers = []
        answers.extend(self.numericals[indices]) ## deep-copy; may modify below
        if two_words or not answers:
            s = "".join(self.ALPHABET[i] for i in indices)
            ## build up concatenatable numerizations
            for first, second in [(self.numerizeWord(s[:i]),
                                   self.numerizeWord(s[i:]))
                                   for i in range(1, len(indices))]:
                if first in self.numericals and second in self.numericals:
                    ## only keep if concatenation maintains indices' order
                    answers.extend(f + " " + s for f in self.numericals[first]
                                               for s in self.numericals[second]
                                   if self.numerizeWord(f+s) == indices)
        return answers

    #########################################################################
    def readin_numerical(self, fname):
        if fname is None:
            fname = os.path.join(HLPDIR, NUMERICALS_FNAME)
        if not os.path.exists(fname):
            print("{} doesn't seem to exist".format(fname))
            return False
        numericals_jsonable = json.load(open(fname))
        for numerical_string, words in numericals_jsonable.items():
            numerical = tuple(int(n) for n in numerical_string.split(","))
            self.numericals[numerical] = set(words)
        return True

    def readin_dict(self, dict_fnames):
        if dict_fnames is None:
            dict_fnames = DICT_FNAMES
        for fname in dict_fnames:
            with open(fname) as fh:
                text = str(fh.read()).replace("\r","").upper()
                for word in text.split("\n"):
                    if not word or not word.isalpha():
                        continue
                    n = self.numerizeWord(word)
                    self.numericals[n].add(word)
        self.save_numericals()

    def save_numericals(self):
        fname = os.path.join(HLPDIR, NUMERICALS_FNAME)
        if os.path.exists(fname):
            return
        if not os.path.exists(HLPDIR):
            os.mkdir(HLPDIR)
        ## json doesn't like tuples and sets; make into strings and lists
        numericals_jsonable = {",".join(str(n) for n in k): list(v)
                                for k, v in self.numericals.items()}
        json.dump(numericals_jsonable, open(fname, "w"), indent=4)
        print("done writing {}".format(fname))
