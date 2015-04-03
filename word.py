#!/usr/bin/python3
import collections
import os
import sys
import json
import string

from .hlpConstants import HLPDIR, DICT_FNAMES, PATTERNS_FNAME

class PatternMapper():
    ALPHABET = string.ascii_uppercase
    DIT = "?"

    def __init__(self, pattern_fname=None, dict_fnames=None):
        self.patterns = collections.defaultdict(set)
        self.words = set()
        self.readin_pattern_file(pattern_fname) or self.readin_dict(dict_fnames)

    def get_pattern(self, word):
        first, last = None, None
        lenword = len(word)
        for idx, letter in enumerate(word):
            if word.count(letter) > 1:
                first = idx
                break
        if first is None:
            return self.ALPHABET[:len(word)] + ":0:0"
        for idx, letter in enumerate(reversed(word), 1):
            if word.count(letter) > 1:
                last = lenword - idx
                break

        substring = word[first:last + 1]
        alphabet_iter = iter(self.ALPHABET)
        mapper = collections.defaultdict(lambda: next(alphabet_iter))
        pattern = "".join(mapper[letter] for letter in substring)
        return pattern + ":{}:{}".format(first, lenword - last - 1)
    
    def find_words(self, word, pattern=None, mapping=None):
        if pattern is None:
            pattern = self.get_pattern(word)
        preset = collections.defaultdict(lambda:self.DIT)
        if mapping is not None:
            preset.update(mapping)
        preset_values = set(preset.values())
        answers = set()
        for potential in self.patterns[pattern]:
            if any(wlett == plett or preset[wlett] not in (self.DIT, plett) or
                   (preset[wlett] == self.DIT and plett in preset_values)
                   for wlett, plett in zip(word, potential)):
                continue
            answers.add(potential)
        return answers

    ##########################################################################
    def save_pattern_file(self, fname=None, fdir=None):
        if fdir is None:
            fdir = HLPDIR
        if fname is None:
            fname = PATTERNS_FNAME
        full_fname = os.path.join(fdir, fname)
        if os.path.exists(full_fname):
            return
        if not os.path.exists(fdir):
            os.mkdir(fdir)
        with open(full_fname, "w") as fh:
            json.dump(self.patterns, fh, indent=4, sort_keys=True)
        print("done writing {}".format(full_fname))

    def readin_pattern_file(self, fname=None):
        if fname is None:
            fname = os.path.join(HLPDIR, PATTERNS_FNAME)
        if not os.path.exists(fname):
            print("{} doesn't seem to exist".format(fname))
            return False
        with open(fname) as fh:
            self.patterns.update(json.load(fh))
        for word_list in self.patterns.values():
            self.words.update(word_list)
        return True

    def readin_dict(self, dict_fnames=None):
        if dict_fnames is None:
            dict_fnames = DICT_FNAMES
        for fname in dict_fnames:
            with open(fname) as fh:
                text = str(fh.read()).replace("\r","").upper()
                word_list = {w for w in text.split("\n") if w.isalpha()}
                self.words.update(word_list)
        for word in self.words:
            self.patterns[self.get_pattern(word)].add(word)
        return True
## want a singleton-esque pattern-mapper
PATTERN_MAPPER = PatternMapper()

##############################################################################
class Word(object):
    PATTERN_MAPPER = PATTERN_MAPPER
    DIT = PATTERN_MAPPER.DIT

    def __init__(self, letters, mapping=None, quick=None):
        self.original_word = letters.upper()
        self.word = "".join(l for l in self.original_word if l.isalpha())
        self.pattern = self.PATTERN_MAPPER.get_pattern(self.word)
        self.mapping = mapping
        if self.mapping is None:
            self.mapping = collections.defaultdict(lambda: self.DIT)

    @property
    def plain(self):
        return "".join(self.mapping[l] for l in self.word)

    @plain.setter
    def plain(self, plainword):
        self.mapping.update(dict(zip(self.word, plainword)))

    @property
    def possibles(self):
        return self.PATTERN_MAPPER.find_words(self.word, self.pattern,
                                              self.mapping)

    @property
    def is_fully_set(self):
        return not self.DIT in self.plain

##############################################################################
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: Provide 1 argument, the word")
        sys.exit(1)
    word = sys.argv[1].upper()
    print(sorted(PATTERN_MAPPER.find_words(word)))
